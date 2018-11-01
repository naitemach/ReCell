from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm
# from .models import User


def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            email = form.cleaned_data['email']
            return render(request, 'store/form.html', {'form': form,'email':email})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'store/form.html', {'form': form})


def index(request):
    return render(request, 'store/products.html', {})


def profile(request):
    return HttpResponse("Hello, world. You're at the polls proiule.")


def home(request):
    return HttpResponse("Hello, world. You're at the polls home.")

def products(request):
    return render(request, 'store/products.html',{})


def register(request):
    return render(request, 'store/register.html',{})

def search(request):
    return HttpResponse("Hello, world. You're at the polls search.")

# def display(request):
#     users = User.objects.all()
#     return render(request,'store/display.html',{'user': users})
