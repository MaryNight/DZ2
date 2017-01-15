#__author__ = 'Work'
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from lab7.models import Lesson

class LessonForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, label='Описание курса')
    image = forms.ImageField(required=False, label='Изображение')
    class Meta:
        model = Lesson
        exclude = ('user_posted',)
    
    def save(self):
        user_model = get_user_model()
        les_pic = self.cleaned_data['image']
        print(les_pic)
        print(self.cleaned_data)
        if not les_pic:
            les_pic = 'lessons_images/None/no-image.jpg'
        lesson = Lesson.objects.create(name=self.cleaned_data['name'],
                                        description=self.cleaned_data['description'],
                                        image = les_pic,
                                        )
        return lesson


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    login = forms.CharField(label='Логин', min_length=5)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    email = forms.CharField(label='Адрес электронной Почты')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    def clean_login(self):
        user_model = get_user_model()
        login = self.cleaned_data['login']
        if user_model.objects.filter(username=login):
            raise ValidationError('Этот login уже занят')
        return login

    def clean_email(self):
        user_model = get_user_model()
        email = self.cleaned_data['email']
        validate_email( self.cleaned_data['email'])
        if user_model.objects.filter(email=email):
            raise ValidationError('Этот email уже зарегистрирован')
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if self.cleaned_data.get('password') and self.cleaned_data.get('repeat_password'):
            if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
                raise ValidationError('Пароли не совпадают')
        return cleaned_data

    def save(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(username=self.cleaned_data['login'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'],
                                        )
        return user
