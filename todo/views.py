from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, TaskForm
from .models import Task

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