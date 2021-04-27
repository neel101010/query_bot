import boto3
import time
import urllib
import json
from urllib.request import urlopen
import logging
from botocore.exceptions import ClientError
import uuid
from pathlib import Path
import os


AWS_ACCESS_KEY_ID = 'AKIA4VRJ74MQUSOS4ETW'
AWS_SECRET_ACCESS_KEY = '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'

temp = Path(__file__).resolve().parent.parent
temp = str(temp)
BASE_DIR = ""
for i in temp:
    if(i=='\\'):
        BASE_DIR = BASE_DIR + '/'
    else:
        BASE_DIR = BASE_DIR + i


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3',region_name='us-east-2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        print("Error occcured while uploading on aws")
        return False
    print("Video Uploaded to aws")
    return True


def generateText(file_raw_name,ext):
    job_name = 'querybotproject'+ str(uuid.uuid4())
    job_uri = 's3://querybot/'+file_raw_name
    transcribe = boto3.client('transcribe' , region_name='us-east-2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY )
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=ext,
        LanguageCode='en-US'
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri']).read()
        data = json.loads(response)
        text = data['results']['transcripts'][0]['transcript']
        print("Text generated successfully")
        print(text)
        return text
    else:
        print("Error Occured while generating text")


def convert_text(course,file_name):
    print(file_name)
    file_raw_name = file_name.split('/')[1]
    file_raw_name,ext = file_raw_name.split('.')
    try:
        os.mkdir(BASE_DIR + "/media/text/" + course)
    except:
        pass
    upd = upload_file(BASE_DIR + "/media/" +  file_name, 'querybot', file_raw_name)
    if upd == False:
        raise Exception("Error occured while uploading to aws")
    text = generateText(file_raw_name,ext)

    f = open(BASE_DIR + "/media/text/" + course + "/" + file_raw_name + '.txt',"w+")
    f.close()
    if not os.path.isfile(BASE_DIR + "/media/text/" + course + "/" + "main.txt"):
        f = open(BASE_DIR + "/media/text/" + course + "/" + "main.txt" ,"w+")
    f.close()
    for t in text:
        with open(BASE_DIR + "/media/text/" + course + "/" + file_raw_name + '.txt', 'a') as f1:
            f1.write(t)
        with open(BASE_DIR + "/media/text/" + course + "/" + "main.txt", 'a') as f2:
            f2.write(t)
    f1.close()
    f2.close()
    print('Text file Generated')
    return BASE_DIR+"/media/text/" + course + "/" + "main.txt", BASE_DIR+"/media/text/"  + course + "/" + file_raw_name + '.txt'
