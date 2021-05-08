from django.shortcuts import render,redirect
from .models import Video,Text,Course,CourseText,Qna
from django.http import HttpResponse
from .utils import *
from .albert import bye
from .text_classifier import do_prediction
from .speech_text import convert_text
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import time
from pathlib import Path

temp = Path(__file__).resolve().parent.parent
temp = str(temp)
BASE_DIR = ""
for i in temp:
    if(i=='\\'):
        BASE_DIR = BASE_DIR + '/'
    else:
        BASE_DIR = BASE_DIR + i

# Create your views here.
# def index(request):
#     return render(request,'index.html')

def videoUpload(request,id):
    if request.method == 'POST':
        video_data = request.FILES['video']
        course = Course.objects.get(pk=id)
        content = Video(video_data=video_data,course=course)
        content.save()
        text_filepath, text_filepath_video = convert_text(course.course_name,content.video_data.name)
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
        'courses': Course.objects.all(),
        'videos':videos,
        'file_content':file_content,
        'AllQuestions' : AllQuestions,
    }
    return render(request,'index.html',context)



@csrf_exempt
def chatInterface(request ,id):
    course = Course.objects.get(pk=id)
    course_text = CourseText.objects.get(course_id = course.id)
    qna = Qna.objects.all()
    f = open(str(course_text.text_data), 'r')
    file_content = f.read()
    f.close()
    answer = ""
    if(request.method == 'POST'):
        question = request.POST.get('question')
        if(len(question) != 0):
            question = request.POST.get('question')
            paragraph = file_content
            if do_prediction(question):
                answer = bye(question,paragraph)
            else:
                answer = "General Question" 

    context = {
        'file_content' : file_content,
        'answer': answer,
    }
    print('Process Finished')
    return JsonResponse(context)


def videoDetails(request,id):
    video = Video.objects.get(pk=id)
    text = Text.objects.get(video_id = video.id)
    AllQuestions = Qna.objects.filter(video_id = video.id)
    print(AllQuestions)
    f = open(str(text.text_data), 'r')
    file_content = f.read()
    f.close()
    context = {
        'video' : video,
        'file_content' : file_content,
        'AllQuestions':  AllQuestions,
    }
    return render(request,'video.html',context)


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
        messages.success(request, "Succussfully logged in" )
        return redirect("/home")
    else:
        messages.error(request, "Wrong credentials" )
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
            messages.error(request, "Username already taken" )
            return redirect("/home/signup")
        elif User.objects.filter(email=email).exists():
            # Redirect them to signup page
            messages.error(request, "Account associated with email already exists" )
            return redirect("/home/signup")
        else:
            user = User.objects.create_user(first_name=firstname , last_name=lastname, email=email, password=password, username=username)
            user.save()
            auth.login(request , user)
            print("User created" , user)
            messages.success(request, "Account successfully created Welcome " )
            return redirect("/home")
    else:
        messages.error(request, "Some error occured please try again" )
        return redirect("/home/signup")


def logout_fun(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out" )
    return redirect("/home")



# 1. Machine Learning — Coursera

@csrf_exempt
def textclassifier(request,course_id, video_id):
    question = request.POST['question']
    if do_prediction(question) == 1:
        value = 1
    else:
        value = 0
    return JsonResponse({ 'value' : value })


# @csrf_exempt
# def gpt2chatbot(request , course_id, video_id):
#     print(request.POST.get('question'))
#     question = request.POST.get('question')
#     answer = bot_response(question)
#     print(answer)
#     return JsonResponse({
#         'question' : question,
#         'answer' : answer,
#     })


# @csrf_exempt
# def similarmatch(request , course_id, video_id):
#     print(request.POST.get('question'))
#     question = request.POST.get('question')
#     # questions_data = ["what is machine learning?" , "what does the role of machine learning and data scientist looks like?" , "what are the requirements of data scientist job?" ]
#     # data = predict_similar_questions(question , questions_data)
#     print(f"Got response from similar questions ===> {data}")
#     return JsonResponse({
#         'question' : "What is Machine Learning?",
#         'answer' : "Something",
#     })



@csrf_exempt
def generateanswer(request ,course_id, video_id):
    if(video_id != 0):
        video = Video.objects.get(pk=video_id)
        text = Text.objects.get(video_id = video.id)
        f = open(str(text.text_data), 'r')
        file_content = f.read()
        f.close()
    else:
        course = Course.objects.get(pk=course_id)
        course_text = CourseText.objects.get(course_id = course.id)
        f = open(str(course_text.text_data), 'r')
        file_content = f.read()
        f.close()
    print(request.POST.get('question'))
    question = request.POST.get('question')
    answer = bye(question,file_content)
    if(video_id != 0):
        new_qna = Qna(question=question,answer=answer,course_id=course_id,video_id=video_id)
    else:
        new_qna = Qna(question=question,answer=answer,course_id=course.id)
    new_qna.save()
    return JsonResponse({
        'question' : question,
        'answer' :  answer,
    })

def question_display(request,course_id,video_id=0):
    if(video_id!=0):
        qna = Qna.objects.filter(course_id=course_id,video_id=video_id)
    else:
        qna = Qna.objects.filter(course_id=course_id)
    context = {
        'questions' : qna,
        'course_id' : course_id,
        'video_id' : video_id,
    }
    return render(request,'questions.html',context)

def question_answer(request,course_id,video_id=0):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        ans = request.POST.get('answer')
        if video_id !=0:
            qna = Qna.objects.get(pk=question_id)
        else:
            qna = Qna.objects.get(pk=question_id)
        qna.answer = ans
        qna.save()
    return redirect(f"/home/questions/{course_id}/{video_id}")


@csrf_exempt
def question_similarity_checker(request, course_id, video_id):
    question = request.POST.get('question')
    answer = ""
    return JsonResponse({
        'question' : question,
        'answer' : "no" 
    })


####
####

####

def start_message():
    print("Bot:",
          "Just start texting me. "
          "If I'm getting annoying, type \"/reset\". "
          )


def reset_message():
    print("Bot:", "Beep beep!")


def initialize(**kwargs):
    """Run the console bot."""
    global general_params
    global device
    global seed
    global debug
    global generation_pipeline_kwargs
    global generator_kwargs
    global prior_ranker_weights
    global cond_ranker_weights
    global chatbot_params
    global max_turns_history
    global generation_pipeline
    global ranker_dict
    global turns
    # Extract parameters
    general_params = kwargs.get('general_params', {})
    device = general_params.get('device', -1)
    seed = general_params.get('seed', None)
    debug = general_params.get('debug', False)

    generation_pipeline_kwargs = kwargs.get('generation_pipeline_kwargs', {})
    generation_pipeline_kwargs = {**{
        'model': 'microsoft/DialoGPT-medium'
    }, **generation_pipeline_kwargs}

    generator_kwargs = kwargs.get('generator_kwargs', {})
    generator_kwargs = {**{
        'max_length': 1000,
        'do_sample': True,
        'clean_up_tokenization_spaces': True
    }, **generator_kwargs}

    prior_ranker_weights = kwargs.get('prior_ranker_weights', {})
    cond_ranker_weights = kwargs.get('cond_ranker_weights', {})

    chatbot_params = kwargs.get('chatbot_params', {})
    max_turns_history = chatbot_params.get('max_turns_history', 2)

    # Prepare the pipelines
    generation_pipeline = load_pipeline('text-generation', device=device, **generation_pipeline_kwargs)
    ranker_dict = build_ranker_dict(device=device, **prior_ranker_weights, **cond_ranker_weights)

    # Run the chatbot
    logger.info("Running the console bot...")

    turns = []
    start_message()

#if args.type == 'console':
# initialize(**config)

def bot_response(prompt) :

    global general_params
    global device
    global seed
    global debug
    global generation_pipeline_kwargs
    global generator_kwargs
    global prior_ranker_weights
    global cond_ranker_weights
    global chatbot_params
    global max_turns_history
    global generation_pipeline
    global ranker_dict
    global turns

    try:
        #while True:
            #prompt = input("User: ")
        if max_turns_history == 0:
            turns = []
        if prompt.lower() == '/start':
            start_message()
            turns = []
            #continue
        if prompt.lower() == '/reset':
            reset_message()
            turns = []
            #continue
        elif prompt.startswith('/'):
            print('Command not recognized.')
            #continue
        # A single turn is a group of user messages and bot responses right after
        turn = {
            'user_messages': [],
            'bot_messages': []
        }
        turns.append(turn)#pass by value not reference
        turn['user_messages'].append(prompt)
        # Merge turns into a single prompt (don't forget delimiter)
        prompt = ""
        from_index = max(len(turns) - max_turns_history - 1, 0) if max_turns_history >= 0 else 0
        for turn in turns[from_index:]:
            # Each turn begins with user messages
            for user_message in turn['user_messages']:
                prompt += clean_text(user_message) + generation_pipeline.tokenizer.eos_token
            for bot_message in turn['bot_messages']:
                prompt += clean_text(bot_message) + generation_pipeline.tokenizer.eos_token

        # Generate bot messages
        bot_messages = generate_responses(
            prompt,
            generation_pipeline,
            seed=seed,
            debug=debug,
            **generator_kwargs
        )
        if len(bot_messages) == 1:
            bot_message = bot_messages[0]
        else:
            bot_message = pick_best_response(
                prompt,
                bot_messages,
                ranker_dict,
                debug=debug
            )
        turn['bot_messages'].append(bot_message)
        return bot_message
    except KeyboardInterrupt:
        exit()
    except:
        raise


logger = setup_logger(__name__)
general_params=None
device=None
seed=None
debug=None
generation_pipeline_kwargs=None
generator_kwargs=None
prior_ranker_weights=None
cond_ranker_weights=None
chatbot_params=None
max_turns_history=None
generation_pipeline=None
ranker_dict=None
turns = []

config_path = BASE_DIR + '/main_app/my_chatbot.cfg'
config = parse_config(config_path)
initialize(**config)
print("GPT 2 SET")


@csrf_exempt
def gpt2chatbot(request , course_id, video_id):
    print(request.POST.get('question'))
    question = request.POST.get('question')
    answer = bot_response(question)
    print(answer)
    return JsonResponse({
        'question' : question,
        'answer' : answer,
    })
