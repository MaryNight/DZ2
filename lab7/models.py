from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    teachs = models.ForeignKey('Lesson',related_name='teachers', on_delete=models.CASCADE, null=True)

class Lesson(models.Model):
	name = models.CharField(max_length=30, verbose_name='Курс')
	description = models.CharField(max_length=255, verbose_name='Описание курса')
	datetime = models.DateTimeField(auto_now=True)
	image = models.ImageField(upload_to = 'lessons_images/', default = 'lessons_images/None/no-image.jpg', verbose_name='Изображение')
	user_posted = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Преподаватель', related_name='lessons', null=True)
    
	def __str__(self):
		return self.name
