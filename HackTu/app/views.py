from django.shortcuts import render
import math
from django.contrib import messages


def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def jee(request):
    return render(request, "jee.html")

def master(request):
    return render(request, "master.html")

def masterdashboard(request):
    return render(request, "dashboard.html")