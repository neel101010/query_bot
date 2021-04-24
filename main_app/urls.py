from django.urls import path
from main_app import views

urlpatterns = [
    path('',views.videoDisplay),
    path('upload/<int:id>',views.videoUpload),
    path('chat/<int:id>',views.chatInterface),
    path('signup',views.signup_view),
    path('login',views.login_view),
    path('signup/check',views.signup_fun),
    path('login/check',views.login_fun),
    path('logout',views.logout_fun),
]