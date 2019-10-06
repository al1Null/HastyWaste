from pymongo import MongoClient

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth import authenticate# , get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# from pymongo import read_preferences

from .forms import UserLoginForm
# from .models import Bin

# UserModel = get_user_model()

# @login_required
def dashboard(request):
    context = {}

    uri = "mongodb+srv://hastyUser2:trashPass123321@hastydb-9azwl.gcp.mongodb.net/admin?retryWrites=true&w=majority"

    client = MongoClient(uri)
    db = client['history']
    col = db['bin01']

    docs = [d for d in col.find({})]
    recent = docs[-1:]
    context['bin01'] = recent[0]

    return render(request, 'trash/dashboard.html', context)


def login(request):

    if request.method == 'POST':

        loginData = UserLoginForm(request.POST)
        print(loginData.is_valid())
        if loginData.is_valid():
            username = loginData.cleaned_data['username']
            password = loginData.cleaned_data['password']
            print(f"User: {username} Pass: {password}")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login_auth(request, user)

                return redirect('dashboard')
            else:
                print("Incorrect Credentials")
                loginData.add_error(None, ValidationError("Invalid Username or Password"))
                # print(loginData.non_field_errors)
                return render(request, 'trash/login.html', {'form': loginData})

        else:
            print("Invalid Fields")

            return render(request, 'trash/login.html', {'form': loginData})
    else:
        form = UserLoginForm()

        return render(request, 'trash/login.html', {'form': form})


def history(request):
    context = {}

    uri = "mongodb+srv://hastyUser2:trashPass123321@hastydb-9azwl.gcp.mongodb.net/admin?retryWrites=true&w=majority"

    client = MongoClient(uri)
    db = client['history']
    col = db['bin01']

    docs = [d for d in col.find({})][2500:2550]
    context['history'] = docs

    return render(request, 'trash/history.html', context)


def contact(request):
    return render(request, 'trash/contact.html')

def about(request):
    return render(request, 'trash/about.html')

@login_required
def logout(request):
    logout_auth(request)
    return redirect('main')
