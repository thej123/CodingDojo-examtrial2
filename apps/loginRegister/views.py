from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'loginRegister/index.html')

def success(request):
    # if someone goes to /success page with logging in, it will redirect to login page
    if 'id' not in request.session:
        return redirect('/loginRegister')
    context = {
        'user' : User.objects.get(id=request.session['id'])
    }
    return render(request, 'loginRegister/success.html', context)

def create(request):
    # sends request to models.py to validate
    # it sends the request.POST it got from 'form' to the models.py
    # the function will either return a 'list' of errors or a object/dictionary of the users info
    result = User.objects.validate_registration(request.POST)
    # check if the returned value is a 'list'
    if type(result) == list:
        # for loop to display all the errors through 'messages'
        for x in result:
            messages.error(request, x)
        return redirect('/loginRegister')
    else:
        # stores the id of the user for future use
        request.session['id'] = result.id
        messages.success(request, 'You have registered successfully!')
        return redirect('/loginRegister/success')

def login(request):
    # sends request to models.py to validate
    # it sends the request.POST it got from 'form' to the models.py
    # the function will either return a 'list' of errors or a object/dictionary of the users info
    result = User.objects.validate_login(request.POST)
    # check if the returned value is a 'list'
    if type(result) == list:
        # for loop to display all the errors through 'messages'
        for x in result:
            messages.error(request, x)
        return redirect('/loginRegister')
    else:
        # stores the id of the user for future use
        request.session['id'] = result.id
        messages.success(request, 'You have logged in!')
        return redirect('/loginRegister/success')

