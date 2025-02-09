from django.shortcuts import render
import openai
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

# TTS
from gtts import gTTS
from django.http import FileResponse
from pydub import AudioSegment

# Key
openai.api_key = ""

@csrf_exempt
def speech_to_text(request):
    if request.method == "POST" and request.FILES.get("audio_file"):
        audio_file = request.FILES["audio_file"]
        file_path = default_storage.save("temp_audio.mp3", audio_file)
        with open(file_path, "rb") as audio:
            transcript = openai.Audio.transcribe("whisper-1", audio)
        return JsonResponse({"transcript": transcript["text"]})
    return JsonResponse({"error": "No audio file found"}, status = 400)

def text_to_speech(request):
    text = request.GET.get("text","Welcome to ExaMentor! Your Ai powered learning platform.")

    #Convert text to speech
    tts = gTTS(text=text,lang =" en")
    audio_file = "tts_output.mp3"
    tts.save(audio_file)

    #Convert to WAV for better browser support
    sound = AudioSegment.from_mp3(audio_file)
    wav_file = "tts_output.wav"
    sound.export(wav_file, format="wav")
    return FileResponse(open(wav_file, "rb"), content_type="audio/wav")
       
