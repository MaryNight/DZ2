"""Templating URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.ExampleView.as_view()),
    url(r'^lessons/', views.LessonsView.as_view(), name='lessons'),
    url(r'^lesson/(?P<id>\d+)', views.LessonView.as_view(), name='lesson_url'),
    url(r'^user/(?P<id>\d+)/teach/(?P<lid>\d+)$', views.teach, name='teach'),
    url(r'^signup/', views.registration, name='signup'),
    url(r'^login/', views.authorization, name='login'),
    url(r'^logout/', views.exit, name='logout'),
    url(r'^new_lesson/', views.new_lesson, name='new_lesson'),
    url(r'^success/', views.SuccessView.as_view(), name='success'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
