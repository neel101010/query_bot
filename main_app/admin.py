from django.contrib import admin

# # Register your models here.
from .models import Video,Course,CourseText, Text, Qna

admin.site.register(Video)
admin.site.register(Course)
admin.site.register(CourseText)
admin.site.register(Text)
admin.site.register(Qna)


# from django.apps import apps


# models = apps.get_models()

# for model in models:
#     admin.site.register(model)