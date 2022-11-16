# Multilingual-Speech-to-Speech-Translator
Multilingual Speech to Speech (STS) Translator is the First Ever Code-mixed English-Arabic speech  to Bangla-Arabic Speech Translator

# Motivation

This repository contains the work of our first ever  Code-mixed English-Arabic speech to Bangla-Arabic Multilingual Speech to Speech (STS) Translator.This implementation makes bangla translated Seerah of Prophet Muhammed (S) that we first collected from here : https://www.youtube.com/playlist?list=PLAEA99D24CA2F9A8F and then translated those English lectures into Bangla.Our main aim was to make AI read gigantic books with less error rate because no one has done that work before for Bangla as a result many Bengali people couldn't read large Bangla important books/lectures like tafsir books, Hadith books and Seerah books in bangla audiobook mode.  our comprehensive Neural Voice cloning system tries to read one of the most popular lectures of Bangla Seerah of Prophet Muhammed (S) like human audiobook reader with very small amount of error rate.it tries to read both Bangla and Arabic fluently. As the reader here is a robot (that uses cloned voice of human) and not a real human so it makes mistakes occasionally. We tried to reduce the error rate as much as we can. It takes a lot of time and effort to make human read gigantic books line by line and release those readings as audiobook and also it is a very complicated process specially for multilingual books. 


# Our end to end pipeline: 
1.	Download all youtube videos from this playlist : https://www.youtube.com/playlist?list=PLAEA99D24CA2F9A8F and Convert videos to audios (.mp4 to .wav conversion)(using this script : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/step1_make_youtube_audio_playlist.py )

2.	Run openAI’s whisper based multilingual STT(speech to text) model to get multilingual text of each video lecture (using this script : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/step2_run_multilingual_stt.py)

3.	Convert each text file from English-Arabic to Bangla Arabic using banglanmt model (a neural machine translator model that can translate texts from English to Bangla with high efficiency) (using this code : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/step3_crosslingual_translator.py )

4.	Run Multilingual (bangla-arabic) TTS(text to speech) system to get audio version of translated bangla seerah by Dr. Yasir Qadhi ( using this code : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/step4_multilingual_tts.py )

5.	Convert audios with single image based videos using ffmpeg (using this notebook : https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/audio_to_video_maker.ipynb )

E2E_Single_Sample_Demo_of_Multilingual_Speech_to_Speech_Translation -> https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/E2E_Single_Sample_Demo_of_Multilingual_Speech_to_Speech_Translation.ipynb 

using this single notebook -> https://github.com/mobassir94/Multilingual-Speech-to-Speech-Translator/blob/main/E2E-Multilingual%20Speech%20to%20Speech%20Translator.ipynb our whole end to end pipeline can be run step by step with ease.

later on if you find any better multilingual stt model than openAI's whisper then use that instead. whisper is not as good as we expected specially for arabic.it makes mistakes several times but still currently this is the best multilingual STT model that we have available for public use.

if you eliminate whisper and scrape the dataset from this source : https://arqadhi.blogspot.com/ and then follow step 3-5 as discussed above then we believe you will gain at least 4-5% accuracy boost for overall system.


# Acknowledgements
[Apsis Solutions Ltd.](https://apsissolutions.com/)

[bengali.ai](https://bengali.ai/)
