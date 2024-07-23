from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, TaskForm
from .models import Task
from django.shortcuts import render
from django.http import HttpResponse

from .models import Alarm
from django.core.mail import send_mail
from django.utils import timezone
from .models import Alarm
import threading
from datetime import datetime
import pytz
from taskly.settings import EMAIL_HOST_USER
from django.conf import settings
from celery import shared_task
from .forms import EmailComposeForm
from django.contrib import messages
from django.core.mail import send_mail

# Mailersend configuration
MAILERSEND_API_KEY = 'mlsn.a2603888ea8129816a8e00e7adf257422f1cc086b284d3eacfa9f7b87a32525a'

def home(request):
    return render(request, 'home.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_login')
    return render(request, 'register.html', {'form': form})

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password")
    return render(request, 'my-login.html', {'form': form})

@login_required(login_url='my_login')
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required(login_url='my_login')
def create_task(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('dashboard')
    return render(request, 'task_form.html', {'form': form})

@login_required(login_url='my_login')
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'task_form.html', {'form': form})

@login_required(login_url='my_login')
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'task_confirm_delete.html', {'task': task})

def user_logout(request):
    logout(request)
    return redirect('home')

def alarm_list(request):
    alarms = Alarm.objects.all()
    return render(request, 'task_form.html', {'alarms': alarms})

def delete_alarm(request, pk):
    alarm = Alarm.objects.get(pk=pk)
    alarm.delete()
    return redirect('alarm_list')


def send_mail(request):
    if request.method == 'POST':
        try:
            subject = 'a Task is coming up!'
            message = 'You have an event coming up.'
            from_email = 'MS_7Fgslr@trial-3vz9dlewq7nlkj50.mlsender.net'
            recipient_list = ['foursoftfoursoft@gmail.com']

            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Email sent successfully!')
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
            return render(request, 'email_not_sent.html')

    return render(request, 'email_not_scheduled.html')