from django.shortcuts import render,redirect
from .models import Video,Text
from django.http import HttpResponse
from .speech_to_text import convert_to_text
from .albert import bye

# Create your views here.
def index(request):
    return render(request,'index.html')


def videoUpload(request):
    if request.method == 'POST':
        # title = request.POST['title']
        video_data = request.FILES['video']
        content = Video(video_data=video_data)
        content.save()
        print(content.id,content.video_data.name)
        text_filepath = convert_to_text(content.video_data.name)
        text_content = Text(video=content, text_data=text_filepath)
        text_content.save()
    return redirect('/home')


def videoDisplay(request):
    videos = Video.objects.all()
    context ={
        'videos':videos,
    }
    return render(request,'index.html',context)


def chatInterface(request,id):
    video = Video.objects.get(pk=id)
    text = Text.objects.get(video=video)
    print(str(text.text_data))
    f = open(str(text.text_data), 'r')
    file_content = f.read()
    f.close()
    answer = "NA"
    if(request.method == 'POST'):
        question = request.POST['question']
        if(len(question) != 0):
            question = request.POST['question']
            paragraph = file_content
            answer = bye(question,paragraph)
    context = {
        'video': video,
        'text': text,
        'file_content' : file_content,
        'answer': answer
    }
    print('Process Finished')
    return render(request,'chat.html', context)

