# jobs/forms.py
from django import forms
from .models import Job, Application, Message

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']

class ReplyMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
