import subprocess
import os
import pydub
from pydub import AudioSegment
from google.cloud import storage, speech
from pathlib import Path


temp = Path(__file__).resolve().parent.parent
temp = str(temp)
BASE_DIR = ""
for i in temp:
    if(i=='\\'):
        BASE_DIR = BASE_DIR + '/'
    else:
        BASE_DIR = BASE_DIR + i
pydub.AudioSegment.ffmpeg = "C:/ffmpeg"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = BASE_DIR+'/main_app/querybot-302205-ac6f1029590c.json'
project_id = 'querybot-302205'
bucket_name = 'querybot_bucket_2'


def convert_audio(filename):
    # // this part renames the filename
    filenamesplit = filename.split('.')[0]
    ext = filename.split('.')[1]
    newfilenamewav = filenamesplit + ".wav"
    newfilename = "mono_" + newfilenamewav
    print("Final name :",newfilename)
    print(f"Extension:",ext)
    ## conversion of file from mp to .wav file so that google speech api can process it and uploading to drive.
    if ext == 'mp3':
        sound = AudioSegment.from_mp3(BASE_DIR + '/media/videos/' + filename)
    if ext == 'mp4':
        sound = AudioSegment.from_file(BASE_DIR + '/media/videos/' + filename, 'mp4')
    
    sound.export(BASE_DIR + '/media/wav_files/' + newfilename , format="wav") 
    print("Wav File Generated")
    storage_client = storage.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    print("Step 1")
    bucket = storage_client.get_bucket(bucket_name)
    print("Step 2")
    blob = bucket.blob(newfilename)
    print("Step 3")
    blob.upload_from_filename(BASE_DIR + '/media/wav_files/'+newfilename)
    print("Step 4")
    print("Uploaded To GCP")
    return  newfilename



def list_blobs(bucket_name):
    ## list all bucket that is present on the GCP
    storage_client = storage.Client(project_id)
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        print(blob.name )


def convert_to_text(course, filename):
    filename = filename.split('/')[-1]
    newfilename = convert_audio(filename)
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = 44100,
        language_code = 'en_US',
        enable_word_time_offsets = True,
        audio_channel_count=2
    )
    response = client.long_running_recognize(config=config, audio={ "uri" : "gs://querybot_bucket_2/" + newfilename})
    result = response.result()
    try:
        os.mkdir(BASE_DIR + "/media/text/" + course)
    except:
        pass
    print("Response Received of speech to text")
    filename = filename.split('.')[0] + '.txt'
    f = open(BASE_DIR + "/media/text/" + course + "/" + filename,"w+")
    f.close()
    f = open(BASE_DIR + "/media/text/" + course + "/" + "main.txt" ,"w+")
    f.close()
    for result in result.results:
        with open(BASE_DIR + "/media/text/" + course + "/" + "main.txt", 'a') as f1:
            f1.write(result.alternatives[0].transcript)
        with open(BASE_DIR + "/media/text/" + course + "/" + filename, 'a') as f2:
            f2.write(result.alternatives[0].transcript)
    f1.close()
    f2.close()
    print('Text file Generated')
    return BASE_DIR+"/media/text/" + course + "/" + "main.txt", BASE_DIR+"/media/text/"  + course + "/" + filename


# list_blobs(bucket_name)
