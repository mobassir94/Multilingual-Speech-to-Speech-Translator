# Multilingual-Speech-to-Speech-Translator
Multilingual Speech to Speech (STS) Translator is the First Ever Code-mixed English-Arabic speech  to Bangla-Arabic Speech Translator

# Motivation

This repository contains the work of our first ever  Code-mixed English-Arabic speech to Bangla-Arabic Multilingual Speech to Speech (STS) Translator.This implementation makes bangla translated Seerah of Prophet Muhammed (S) that we first collected from here : https://www.youtube.com/playlist?list=PLAEA99D24CA2F9A8F and then translated those English lectures into Bangla.Our main aim was to make AI read gigantic books with less error rate because no one has done that work before for Bangla as a result many Bengali people couldn't read large Bangla important books/lectures like tafsir books, Hadith books and Seerah books in bangla audiobook mode.  our comprehensive Neural Voice cloning system tries to read one of the most popular lectures of Bangla Seerah of Prophet Muhammed (S) like human audiobook reader with very small amount of error rate.it tries to read both Bangla and Arabic fluently. As the reader here is a robot (that uses cloned voice of human) and not a real human so it makes mistakes occasionally. We tried to reduce the error rate as much as we can. It takes a lot of time and effort to make human read gigantic books line by line and release those readings as audiobook and also it is a very complicated process specially for multilingual books. 


# Our end to end pipeline: 
1.	Download all youtube videos from this playlist : https://www.youtube.com/playlist?list=PLAEA99D24CA2F9A8F
2.	Convert videos to audios (.mp4 to .wav conversion)
3.	Run openAI’s whisper based multilingual STT(speech to text) model to get multilingual text of each video lecture
4.	Convert each text file from English-Arabic to Bangla Arabic using banglanmt model (a neural machine translator model that can translate texts from English to Bangla with high efficiency)
5.	Run Multilingual (bangla-arabic) TTS(text to speech) system to get audio version of translated bangla seerah by Dr. Yasir Qadhi
6.	Convert audios with single image based videos using ffmpeg



# Acknowledgements
[Apsis Solutions Ltd.](https://apsissolutions.com/)

[bengali.ai](https://bengali.ai/)
