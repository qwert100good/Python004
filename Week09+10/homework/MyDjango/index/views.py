from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form})
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            payload = login_form.cleaned_data
            user = authenticate(username=payload['username'], password=payload['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                login_form.add_error('username', '用户名或密码错误，请重试')
                return render(request, 'login.html', {'form': login_form})


def register(request):
    if request.method == 'GET':
        reg_form = RegisterForm()
        return render(request, 'register.html', {'form': reg_form})
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            cd = reg_form.cleaned_data
            user = User.objects.create_user(username=cd['username'], password=cd['pwd'])
            user.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'register.html', {'form': reg_form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required()
def index(request):
    return render(request, 'index.html')
