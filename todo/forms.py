from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name','title', 'description', 'completed']
        
class EmailScheduleForm(forms.Form):
    send_time = forms.DateTimeField(label='Send Time', help_text='Enter date and time to send the email')

class EmailComposeForm(forms.Form):
    to_email = forms.EmailField(label='To Email', help_text='Recipient email address')
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)
    send_time = forms.DateTimeField(label='Send Time', help_text='Enter date and time to send the email')























