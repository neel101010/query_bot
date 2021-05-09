from django.urls import path
from main_app import views

urlpatterns = [
    path('',views.videoDisplay),
    path('upload/<int:id>',views.videoUpload),
    path('chat/classifytext/<int:course_id>/<int:video_id>' , views.textclassifier),
    path('chat/gpt2chatbot/<int:course_id>/<int:video_id>' , views.gpt2chatbot),
    path('chat/similarmatch/<int:course_id>/<int:video_id>' , views.similarmatch),
    path('chat/generateanswer/<int:course_id>/<int:video_id>' , views.generateanswer),
    path('chat/<int:course_id>/<int:video_id>',views.chatInterface),
    path('signup',views.signup_view),
    path('login',views.login_view),
    path('signup/check',views.signup_fun),
    path('login/check',views.login_fun),
    path('logout',views.logout_fun),
    path('video/<int:id>',views.videoDetails),
    path('questions/<int:course_id>/<int:video_id>',views.question_display),
    path('questions/answer/<int:course_id>/<int:video_id>',views.question_answer),
    path('questions/questionpost/<int:course_id>/<int:video_id>' , views.question_post)
]