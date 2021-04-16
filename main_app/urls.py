from django.urls import path
from main_app import views

urlpatterns = [
    path('',views.videoDisplay),
    path('upload',views.videoUpload),
    path('chat/<int:id>',views.chatInterface),
]