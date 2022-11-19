#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', '\n!pip install -q transformers\n\n!pip install sentencepiece\n!pip install git+https://github.com/csebuetnlp/normalizer\n\n! pip install bangla==0.0.2\n# !pip install num2words\n!nvidia-smi')


# In[2]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import re
# from num2words import num2words
import os
from tqdm.auto import tqdm
tqdm.pandas()

import transformers

import torch
import bangla
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer,pipeline
from normalizer import normalize # pip install git+https://github.com/csebuetnlp/normalizer

import warnings
warnings.filterwarnings("ignore")

# from pandarallel import pandarallel
# pandarallel.initialize(progress_bar=True,nb_workers=8)

os.environ["TOKENIZERS_PARALLELISM"] = "true"

print(torch.__version__)

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[3]:


seerah = pd.read_csv('../input/yasir-qadhi-seerah/seerah.csv')
seerah.head()


# In[4]:


print(torch.__version__)
transformers.__version__


# In[5]:


get_ipython().run_cell_magic('time', '', '\ndef text_cleaner(text):\n    res = re.sub(\'\\\'\',\'\',text)\n    res = re.sub(\'\\n\',\'.\',res)\n    \n    res = re.sub(\'﴾\',\'\',res)\n    res = re.sub(\'﴿\',\'\',res)\n    \n    res = re.sub(\'«\',\'\',res)\n    res = re.sub(\'»\',\'\',res)\n    \n#     res = res.replace(\'Prev.Next\',\'\')\n    return res\n    \nseerah["text"]=seerah.text.progress_apply(lambda text: text_cleaner(text))')


# In[6]:


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


# In[7]:


get_ipython().run_cell_magic('time', '', '\nseerah["text"]=seerah.text.progress_apply(lambda seerah_eng: tag_arabic_text(seerah_eng,english_only=False))')


# In[8]:


# seerah["text"][0]


# In[9]:


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

text=translate_en_bn("alhamdulillah for everything.")
print(text)


# In[10]:


en_text = '''In the Name of Allah, the Most Gracious, the Most Merciful. <ar> ﴿الْحَمْدُ للَّهِ رَبِّ الْعَـلَمِينَ﴾ </ar>
(Allah, the Exalted, said, `I have divided the prayer (Al-Fatihah) into two halves between 
Myself and My servant, and My servant shall have what he asks for.
If he says,' <ar> بِسْمِ اللَّهِ الرَّحْمَـنِ الرَّحِيمِ </ar> Allah says, `My servant has praised Me.' '''

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
    
    bn_mlt = bn_mlt.replace("<ar>"," ")
    bn_mlt = bn_mlt.replace("</ar>"," ")
    return bn_mlt
        
EN_AR_to_BN_AR_Translator(en_text,tag_text = False)


# In[11]:


# %%time

# seerah["seerah_bn"] = seerah["text"]
# for i in range(1):
#     seerah["seerah_bn"][i] = EN_AR_to_BN_AR_Translator(seerah.text[i],tag_text = False)


# In[12]:


get_ipython().run_cell_magic('time', '', 'seerah["seerah_bn"]=seerah.text.progress_apply(lambda en_text: EN_AR_to_BN_AR_Translator(en_text))')


# In[13]:


seerah.to_csv('./en_bn_seerah.csv',index = False)


# In[14]:


seerah

