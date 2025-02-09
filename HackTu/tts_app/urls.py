from django.urls import path
from .views import speech_to_text, text_to_speech

urlpatterns = [
    path("speech-to-text/", speech_to_text, name="speech-to-text"),
    path("text-to-speech/", text_to_speech, name="text-to-speech"),
]