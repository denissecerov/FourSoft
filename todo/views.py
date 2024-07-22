from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, TaskForm
from .models import Task
from django.shortcuts import render
from django.http import HttpResponse

from .models import Alarm
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from .models import Alarm
import threading
from datetime import datetime
import pytz
from taskly.settings import EMAIL_HOST_USER

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
    return render(request, 'alarm_list.html', {'alarms': alarms})

def add_alarm(request):
    if request.method == 'POST':
        time = request.POST['time']
        alarm = Alarm.objects.create(time=time)
        alarm_time = datetime.strptime(time, "%H:%M").time()

        # Schedule sending email at the specified time
        schedule_email(alarm.pk, alarm_time)

        return redirect('alarm_list')
    return render(request, 'add_alarm.html')

def delete_alarm(request, pk):
    alarm = Alarm.objects.get(pk=pk)
    alarm.delete()
    return redirect('alarm_list')

def set_email(request):
    if request.method == 'POST':
        time = request.POST.get("time")
        print(f"Time is: {time}")

def send_alarm_email(alarm_id):
    alarm = Alarm.objects.get(pk=alarm_id)
    subject = 'Alarm Notification'
    message = f'Your alarm is set for {alarm.time.strftime("%I:%M %p")}.'
    from_email = EMAIL_HOST_USER
    to_email = ['foursoftfoursoft@gmail.com']

    print(f'alarm is: {alarm}')
    send_mail(subject, message, from_email, to_email, fail_silently=True)
    return HttpResponse('Email sent successfully')

def schedule_email(alarm_id, alarm_time):
    utc = pytz.UTC
    current_time = timezone.now()
    alarm_datetime = datetime.combine(timezone.now().date(), alarm_time)
    alarm_datetime = utc.localize(alarm_datetime)
    if alarm_datetime < current_time:
        return  # If the alarm time is in the past, do not schedule the email

    seconds_until_alarm = (alarm_datetime - timezone.now()).total_seconds()
    threading.Timer(seconds_until_alarm, send_alarm_email, args=[alarm_id]).start()


