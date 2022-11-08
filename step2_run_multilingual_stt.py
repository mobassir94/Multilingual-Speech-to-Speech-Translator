import re
import whisper
import librosa
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil
import os
import soundfile as sf

folder_path = os.path.join(os.getcwd() , 'Seerah_of_Prophet_Muhammed_SAW') 
model = whisper.load_model("large")

def collapse_whitespace(text):
    # Regular expression matching whitespace:
    _whitespace_re = re.compile(r"\s+")
    return re.sub(_whitespace_re, " ", text)

def mlt_speech_to_text_convertor(path = "seerah_of_the_prophet.wav",silence_based_conversion = False):
    '''
        #modified from https://www.geeksforgeeks.org/python-speech-recognition-on-large-audio-files/

        -> a function that splits the audio file into chunks and applies multilingual speech recognition.
        -> supports both silence_based_conversion and fixed length chunking
    '''
    shutil.rmtree('audio_chunks', ignore_errors=True)
    # create a directory to store the audio chunks.
    try:
        os.mkdir('audio_chunks')
    except(FileExistsError):
        pass
  
    

    if(not silence_based_conversion):
        # move into the directory to
        # store the audio files.
        os.chdir('audio_chunks')

#         full_audio, fs = librosa.load(path)
        full_audio, fs = librosa.load(os.path.join(folder_path , path))
        TEXTS=[]
        MAX_AUDIO_LEN=30*fs
        for idx in range(0,full_audio.shape[0],MAX_AUDIO_LEN):
          audio=full_audio[idx:idx+MAX_AUDIO_LEN]
          sf.write(f"{idx}.wav",audio,fs)
          audio = whisper.load_audio(f"{idx}.wav")
          audio = whisper.pad_or_trim(audio)
          # make log-Mel spectrogram and move to the same device as the model
          mel = whisper.log_mel_spectrogram(audio).to(model.device)

          # decode the audio
          options = whisper.DecodingOptions()
          result = whisper.decode(model, mel, options)
      
          #take only arabic and english
          result=re.sub('[^\u0600-\u06FF a-zA-Z0-9,?!.\']',' ',result.text)
          result = collapse_whitespace(result)
          
          # print the recognized text
          TEXTS.append(result)
        os.chdir('..')
        return TEXTS

    # move into the directory to
    # store the audio files.
    os.chdir('audio_chunks')
    
    # open the audio file stored in
    # the local system as a wav file.
    lecture = AudioSegment.from_wav(os.path.join(folder_path , path))

    # split track where silence is 0.5 seconds 
    # or more and get chunks
    chunks = split_on_silence(lecture,
        # must be silent for at least 0.5 seconds
        # or 500 ms. adjust this value based on user
        # requirement. if the speaker stays silent for 
        # longer, increase this value. else, decrease it.
        min_silence_len = 500,
  
        # consider it silent if quieter than -16 dBFS
        # adjust this per requirement
        silence_thresh = -16
    )
  
  
    TEXTS=[]
    i = 0
    # process each chunk
    for chunk in chunks:
              
        # Create 0.5 seconds silence chunk
        chunk_silent = AudioSegment.silent(duration = 10)
  
        # add 0.5 sec silence to beginning and 
        # end of audio chunk. This is done so that
        # it doesn't seem abruptly sliced.
        audio_chunk = chunk_silent + chunk + chunk_silent
  
        # export audio chunk and save it in 
        # the current directory.

        # specify the bitrate to be 192 k
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
  
        # the name of the newly created chunk
        filename = 'chunk'+str(i)+'.wav'


        # recognize the chunk
     
        audio = whisper.load_audio(filename)
        audio = whisper.pad_or_trim(audio)
        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # decode the audio
        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)
        #take only arabic and english
        result=re.sub('[^\u0600-\u06FF a-zA-Z0-9,?!.\']',' ',result.text)
        result = collapse_whitespace(result)
        TEXTS.append(result)
        i+=1
    
    os.chdir('..')
    shutil.rmtree('audio_chunks', ignore_errors=True)
    return TEXTS
