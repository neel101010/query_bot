from django.db import models

# Create your models here.

class Course(models.Model):
    course_name = forms.CharField()
    def __str__(self):
        return str(self.course_name)

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video_data = models.FileField(upload_to='videos/')

    def __str__(self):
        return str(self.video_data)

class Text(models.Model):
    video = models.OneToOneField(Video, on_delete = models.CASCADE, primary_key = True)
    text_data = models.FileField(upload_to='text/')

    def __str__(self):
        return str(self.text_data)