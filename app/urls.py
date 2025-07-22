from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("", views.home, name="home"),
    path("tts-audio/", views.tts_audio, name="tts_audio"),  
    path('voice/', views.voice_query, name='voice_query'),
    path("get-audio/", views.query_audio, name="query_audio"),
    path("upload-audio/", views.upload_audio, name="upload_audio"),
]
     