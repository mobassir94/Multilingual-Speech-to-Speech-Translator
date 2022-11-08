import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import re
from normalizer import normalize # pip install git+https://github.com/csebuetnlp/normalizer
import bangla

def tag_arabic_text(text,ar_pattern=u'[\u0600-\u06FF]+',english_only = False):
    # remove multiple spaces
    data=re.sub(' +', ' ',text)
    texts=[]
    if "।" in data:punct="।"
    elif "." in data:punct="."
    else:punct="\n"
    for text in data.split(punct):    
        # create start and end
        text="start"+text+"end"
        # tag text
        parts=re.split(ar_pattern, text)
        parts=[p for p in parts if p.strip()]
        parts=set(parts)
        for m in parts:
            if len(m.strip())>1:text=text.replace(m,f"</ar>{m}<ar>")
        # clean-up invalid combos
        text=text.replace("</ar>start",'')
        text=text.replace("end<ar>",'')
        texts.append(text)
    text=f"{punct}".join(texts)
    if(english_only):
        #https://stackoverflow.com/questions/55656429/replace-or-remove-html-tag-content-python-regex
        return re.sub(r'(?s)<ar>.*?</ar>', '', text)
    return text

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(torch_device)
model = AutoModelForSeq2SeqLM.from_pretrained("csebuetnlp/banglat5_nmt_en_bn").to(torch_device)
tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/banglat5_nmt_en_bn",use_fast=True)

def translate_en_bn(input_sentence):
    input_ids = tokenizer(normalize(input_sentence), return_tensors="pt").input_ids
    input_ids = input_ids.to(torch_device)
    generated_tokens = model.generate(input_ids)
    decoded_tokens = tokenizer.batch_decode(generated_tokens)[0]
    decoded_tokens=decoded_tokens.replace("<pad>","").replace("</s>","")
    sen=decoded_tokens.split()
    words=[w for w in sen if w.strip()]
    sen=" ".join(words)
    return decoded_tokens

def EN_AR_to_BN_AR_Translator(en_text,tag_text = False):
    '''
    translates multilingual english-arabic code mixed text into 
    multilingual bengali-arabic code mixed text
    ''' 
    if(tag_text):
        en_text = tag_arabic_text(en_text,english_only=False)
    
    sentenceEnders = re.compile('[.!?]')
    sentences = sentenceEnders.split(en_text)
    main_list = []
    for i in range(len(sentences)):
        list_str = sentences[i].split('<ar>')
        if(len(list_str) == 1):
            main_list.append(list_str[0])
        else:
            for j in range(len(list_str)):
                if('</ar>' in list_str[j]):
                    list_str1 = list_str[j].split('</ar>')
                    main_list.append("<ar>"+list_str1[0]+"</ar>")
                    main_list.append(list_str1[1])
                else:
                    main_list.append(list_str[j])

    while(" " in main_list):
        main_list.remove(" ")
    for idx in range(len(main_list)):
        if('<ar>' not in main_list[idx] or '</ar>' not in main_list[idx]):
            
            output_sentence = []
            for word in main_list[idx].split():
                output_sentence.append(word)
     
            main_list[idx] = ' '.join(output_sentence)
            #numerizer
            main_list[idx] = bangla.convert_english_digit_to_bangla_digit(main_list[idx])
            # multilingual english-arabic to multilingual bengali-arabic
            try:
                if len(main_list[idx])>1:
                    main_list[idx]=translate_en_bn(main_list[idx])
                            
            except:
                print("failed -> ",main_list[idx])
    
    bn_mlt = " ".join(main_list)
    bn_mlt = re.sub(' ্ ','',bn_mlt)
    bn_mlt = re.sub("\\'","",bn_mlt)#replace \'
    bn_mlt = re.sub('<unk>','',bn_mlt)
#     bn_mlt=bn_mlt.replace("<ar>",'')
#     bn_mlt=bn_mlt.replace("</ar>",'')
    return bn_mlt
        

