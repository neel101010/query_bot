from django.shortcuts import render,redirect
from .models import Video,Text,Course,CourseText,Qna
from django.http import HttpResponse
from .speech_to_text import convert_to_text
from .albert import bye
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
import time

# Create your views here.
def index(request):
    return render(request,'index.html')


def videoUpload(request,id):
    if request.method == 'POST':
        video_data = request.FILES['video']
        course = Course.objects.get(pk=id)
        content = Video(video_data=video_data,course=course)
        content.save()
        text_filepath, text_filepath_video = convert_to_text(course.course_name,content.video_data.name)
        
        course_text_content = CourseText(course=course, text_data=text_filepath)
        course_text_content.save()

        text_content = Text(video=content, text_data=text_filepath_video)
        text_content.save()
    return redirect('/home')


def videoDisplay(request):
    videos = Video.objects.all()
    AllQuestions = Qna.objects.all()
    courses = Course.objects.all()
    file_content = {}
    for course in courses:
        try:
            course_text = CourseText.objects.get(course_id = course.id)
            f = open(str(course_text.text_data) , 'r')
            file_content[course.id] = f.read()
            f.close()
        except:
            print("Error Occurred")
            continue
    
    context = {
        'courses': [Course.objects.all().first],
        'videos':videos,
        'file_content':file_content,
        'AllQuestions' : AllQuestions,
    }
    return render(request,'index.html',context)



@csrf_exempt
def chatInterface(request ,id):
    # text = Text.objects.get(video=video)
    course = Course.objects.get(pk=id)
    course_text = CourseText.objects.get(course_id = course.id)
    qna = Qna.objects.all()
    # video = Video.objects.get(pk=id)
    f = open(str(course_text.text_data), 'r')
    file_content = f.read()
    f.close()
    answer = "NA"
    if(request.method == 'POST'):
        question = request.POST.get('question')
        if(len(question) != 0):
            question = request.POST.get('question')
            paragraph = file_content
            answer = bye(question,paragraph)
    context = {
        # 'video': video,
        # 'text': text,
        'file_content' : file_content,
        'answer': answer,
    }
    print('Process Finished')
    return JsonResponse(context)
    # return render(request,'chat.html', context)


def login_view(request):
    return render(request,'login.html')

def signup_view(request):
    return render(request,'signup.html')

def login_fun(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        print("User is logged in")
        return redirect("/home")
    else:
        return redirect("/home/login")

def signup_fun(request):
    username = request.POST['username']
    password = request.POST['password']
    cpassword = request.POST['cpassword'] 
    email = request.POST['email']
    firstname = username
    lastname = username

    if password == cpassword:
        if User.objects.filter(username=username).exists():
            # Redirect them to signup page
            return redirect("/home/signup")
        elif User.objects.filter(email=email).exists():
            # Redirect them to signup page
            return redirect("/home/signup")
        else:
            user = User.objects.create_user(first_name=firstname , last_name=lastname, email=email, password=password, username=username)
            user.save()
            auth.login(request , user)
            print("User created" , user)
            return redirect("/home")
    else:
        return redirect("/home/signup")


def logout_fun(request):
    auth.logout(request)
    return redirect("/home")


def videoDetails(request,id):
    video = Video.objects.get(pk=id)
    text = Text.objects.get(video_id = video.id)
    f = open(str(text.text_data), 'r')
    file_content = f.read()
    f.close()
    context = {
        'video' : video,
        'file_content' : file_content,
    }
    return render(request,'video.html',context)

# 1. Machine Learning — Coursera

@csrf_exempt
def textclassifier(request, id):
    time.sleep(2)
    print(request.POST.get('question'))
    return JsonResponse({ 'value' : 1 })


@csrf_exempt
def gpt2chatbot(request , id):
    time.sleep(2)
    print(request.POST.get('question'))
    question = request.POST.get('question')
    return JsonResponse({
       'question' : question,
       'answer' : "Hi Ajay, I am GPT3 chatbot." 
    })


@csrf_exempt
def similarmatch(request , id):
    time.sleep(2)
    print(request.POST.get('question'))
    question = request.POST.get('question')
    return JsonResponse({
       'question' : "What is Machine Learning?",
       'answer' : "Something" 
    })



@csrf_exempt
def generateanswer(request , id):
    time.sleep(2)
    print(request.POST.get('question'))
    question = request.POST.get('question')
    return JsonResponse({
       'question' : "What is Machine Learning?",
       'answer' : "Machine learning is the study of computer algorithms that improve automatically through experience and by the use of data. It is seen as a part of artificial intelligence." 
    })