import ffmpeg
from pytube import YouTube
from pytube import Playlist
import moviepy.editor as mp
import os
import re

#Download youtube video playlist and convert them into .wav audio format

'''
original implementation https://github.com/pushpendra050/Pytube-for-Playlist-download/blob/main/PyTubeMain.py
modified by Md. Rezwanul Haque (Rezwan) and Syed Mobassir (Shabab)
'''
SAVE_PATH = "Seerah_of_Prophet_Muhammed_SAW" #to_do

links = "https://www.youtube.com/playlist?list=PLAEA99D24CA2F9A8F"


playlist = Playlist(links)

PlayListLinks = playlist.video_urls
N = len(PlayListLinks)

print(f"This link found to be a Playlist Link with number of videos equal to {N} ")
print(f"\n Lets Download all {N} videos")

#mylist = range(85,106)
for i,link in enumerate(PlayListLinks):
    # Process batch-wise in order to avoid possible http 500 error for large playlist
    '''
    if(i+1 not in mylist):
        continue
    '''
    yt = YouTube(link)
    d_video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    # video_titleName = yt.title
    # print(video_titleName)
    outfileName = d_video.download(SAVE_PATH)
    outfileName_cpy = outfileName

    print(i+1, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Video is Downloaded.')

    head, output = os.path.split(outfileName)
    output= re.sub('[^a-zA-Z0-9.]','_',output)
    output = output.split(".")[0]+".wav"
    output = head+"/"+str(i+1)+"."+output
    
    outfileName = "'" + outfileName + "'"
    cmd = f'ffmpeg -i {outfileName} -ac 2 -f wav {output}'
    os.system(cmd)

    print(i+1, '--------------------->>>>>> Audio is Converted.deleting video')
    
    os.remove(outfileName_cpy)
    

