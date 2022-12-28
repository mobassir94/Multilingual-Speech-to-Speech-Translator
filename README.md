# Multilingual-Speech-to-Speech-Translator
Multilingual Speech to Speech (STS) Translator is the First Ever Code-mixed English-Arabic speech  to Bangla-Arabic Speech Translator

# Motivation

This repository contains the work of our first ever  Code-mixed English-Arabic speech to Bangla-Arabic Multilingual Speech to Speech (STS) Translator.This implementation makes bangla translated Seerah of Prophet Muhammed (S) that we first collected from here : https://www.youtube.com/playlist?list=PLAEA99D24CA2F9A8F and then translated those English lectures into Bangla.


# Our end to end pipeline: 
1.	Download all youtube videos from this playlist : https://www.youtube.com/playlist?list=PLAEA99D24CA2F9A8F and Convert videos to audios (.mp4 to .wav conversion)(using this script : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/step1_make_youtube_audio_playlist.py )

2.	Run openAI’s whisper based multilingual STT(speech to text) model to get multilingual text of each video lecture (using this script : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/step2_run_multilingual_stt.py)

3.	Convert each text file from English-Arabic to Bangla Arabic using banglanmt model (a neural machine translator model that can translate texts from English to Bangla with high efficiency) (using this code : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/step3_crosslingual_translator.py )

4.	Run Multilingual (bangla-arabic) TTS(text to speech) system to get audio version of translated bangla seerah by Dr. Yasir Qadhi ( using this code : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/step4_multilingual_tts.py )

5.	Convert audios with single image based videos using ffmpeg (using this notebook : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/audio_to_video_maker.ipynb )

E2E_Single_Sample_Demo_of_Multilingual_Speech_to_Speech_Translation -> https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/E2E_Single_Sample_Demo_of_Multilingual_Speech_to_Speech_Translation.ipynb 

using this single notebook -> https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/E2E-Multilingual%20Speech%20to%20Speech%20Translator.ipynb our whole end to end pipeline can be run step by step with ease.

we've discovered one crucial limitation of whisper during working on this multilingual speech to speech translation project. the original seerah lecture that we tried to convert from english-arabic to bangla-arabic format is of more than 10 years old. perhaps whisper doesn't work well on such old contents but works fine with latest contents? we've seen that whisper failed very badly on such old contents(10+ years old videos) but when working on latest or recent most videos,whisper worked as well as expected. for example,check last code cell's output from this notebook -> https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/E2E_Single_Sample_Demo_of_Multilingual_Speech_to_Speech_Translation.ipynb and you will see it did good enough job for translating that english-arabic lecture into bangla-arabic lecture.

in order to read that seerah lecture series in bangla we scrapped the dataset from this highly reliable source instead : https://arqadhi.blogspot.com/ and then followed step 3-5. However, our multilingual speech to speech translation pipeline should work just fine with latest or not too old audios containing english-arabic lectures as shown in E2E_Single_Sample_Demo_of_Multilingual_Speech_to_Speech_Translation.ipynb notebook,if it doesn't then try to find better replacement of whisper.

[Transcribed by Br. Safwan Khan, Faizan & Zohra]
safwan-khan@hotmail.com
[Re-revised by Muhammad Abdul Rahman, April 2021]

This channel -> https://www.youtube.com/playlist?list=PLsHVxzxNumvPSbuqcL8oSWoxCPpZ2A3HT covers all lectures of The Bangla-translated Seerah of Prophet Muhammed (PBUH) that we collected from here: https://arqadhi.blogspot.com/ and then translated those English lectures into Bangla using a powerful neural machine translator. This Neural Voice cloning system tries to read one of the most popular lectures of Bangla Seerah of Prophet Muhammed (PBUH) like a human audiobook reader with a minimal amount of error rate. It tries to read both Bangla and Arabic fluently. As the reader here is a robot (that uses the cloned voice of human) and not an actual human so it makes mistakes occasionally. We tried to reduce the error rate as much as we can. It takes a lot of time and effort to make humans read gigantic books line by line and release those readings as audiobooks. It is also a very complicated process, especially for multilingual books. Our main aim was to make AI read gigantic books with less error rate because no one has done that work before for Bangla, as a result many Bengali people couldn't read large Bangla important books like tafsir books, Hadith books and Seerah books in audiobook mode.This is our first baby step towards this research direction. in order to learn more about our Neural Speech synthesized Multilingual (Bangla+arabic) reader,check this repo -> https://github.com/mobassir94/comprehensive-bangla-tts



# Acknowledgements
[Apsis Solutions Ltd.](https://apsissolutions.com/)

[bengali.ai](https://bengali.ai/)
