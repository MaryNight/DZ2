from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from lab7.models import *
from lab7.forms import *
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,logout
from django.contrib import auth

# Create your views here.

class ExampleView(View):
    def get(self, request):
        return render(request, 'base.html')

class SuccessView(View):
    def get(self, request):
        return render(request, 'success.html')

class LessonsView(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'lessons.html'
    paginate_by = 5
    
    def get_queryset(self):
        qs = Lesson.objects.all().order_by('id')
        return qs

class LessonView(View):
    def get(self, request, id):
        data = Lesson.objects.get(id__exact=id)
        return render(request, 'lesson.html', {'lesson':data})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lessons')
        return render(request, 'signup.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def authorization(request):
    redirect_url = '/lessons'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'],
                                     password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_url)
            else:
                form.add_error(None, 'Wrong login or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form, 'continue': redirect_url})

@login_required
def exit(request):
    logout(request)
    return render(request, 'logout.html')
    
@login_required
def new_lesson(request):
    instance = Lesson(user_posted=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST,request.FILES)
        if form.is_valid():
            lesson = form.save()
            lesson.user_posted = request.user
            print(lesson.user_posted.id)
            lesson.save()
            return redirect(reverse('lesson_url', args=(lesson.id,)))
        return render(request, 'new_lesson.html', {'form': form})
    else:
        form = LessonForm()
    return render(request, 'new_lesson.html', {'form': form})

@login_required
def teach(request, id, lid):
    teacher = MyUser.objects.filter(id=id)[0]
    lesson = Lesson.objects.filter(id=lid)[0]
    if teacher in lesson.teachers.all():
        return HttpResponse('Вы уже ведёте этот урок и наверняка балуетесь с адресной строкой')
    lesson.teachers.add(teacher)
    return HttpResponse('Теперь вы ведёте {}'.format(
       lesson.name
))
