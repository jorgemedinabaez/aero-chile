from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    return HttpResponse('Hola mundo')