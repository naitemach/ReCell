from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'store/index.html', {})


def profile(request):
    return HttpResponse("Hello, world. You're at the polls proiule.")


def home(request):
    return HttpResponse("Hello, world. You're at the polls home.")


def search(request):
    return HttpResponse("Hello, world. You're at the polls search.")
