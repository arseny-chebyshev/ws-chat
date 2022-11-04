from traceback import format_stack
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Chat, User

class ChatForm(forms.ModelForm):

    class Meta: 
        model = Chat
        fields = ['name']

