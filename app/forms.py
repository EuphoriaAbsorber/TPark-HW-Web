from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from app.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 40)
    password = forms.CharField(max_length = 40, widget=forms.PasswordInput())

    def clean_username(self):
        data = self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            raise forms.ValidationError("No user with this username")
        return data

    def clean_password(self):
        dataUsername = self.data['username']
        dataPassword = self.cleaned_data['password']

        if User.objects.filter(username=dataUsername).exists() and not authenticate(username=dataUsername,password=dataPassword):
            raise forms.ValidationError("Wrong password")
        return dataPassword

class SignUpForm(forms.Form):
    username = forms.CharField(max_length = 40)
    email = forms.CharField(max_length = 40, required=False)
    password = forms.CharField(max_length = 40, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length = 40, label='Repeat Password', widget=forms.PasswordInput())

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("This username is already used")
        return data

    def clean_password(self):
        dataPassword = self.cleaned_data['password']
        if len(dataPassword) < 6:
            raise ValidationError("Password must be longer than 6 symlols")
        return dataPassword
        
    def clean_password2(self):
        dataPassword = self.data['password']
        dataPassword2 = self.cleaned_data['password2']
        if dataPassword != dataPassword2:
            raise ValidationError("Passwords do not match")
        return dataPassword2

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(label='Tags', max_length=100)
    class Meta:
        model = Question
        fields = ["title", "text", "tags"]

    def clean_title(self):
        data = self.cleaned_data['title']
        return data

    def clean_text(self):
        data = self.cleaned_data['text']
        return data

    def clean_tags(self):
        tagList = []
        data = self.cleaned_data['tags']
        tagList = data.split()
        return tagList
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]

    def clean_text(self):
        data = self.cleaned_data['text']
        return data

class SettingsForm(forms.Form):
    username = forms.CharField(max_length = 40, required=False)
    email = forms.CharField(max_length = 40, required=False)
    password0 = forms.CharField(max_length = 40, label='Old Password', widget=forms.PasswordInput(), required=False)
    password = forms.CharField(max_length = 40, label='New Password', widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(max_length = 40, label='Repeat New Password', widget=forms.PasswordInput(), required=False)

    def clean_username(self):
        data = self.cleaned_data['username']
        dataPassword = self.data['password0']
        if User.objects.filter(username=data).exists() and not authenticate(username=data,password=dataPassword):
            raise forms.ValidationError("This username is already used")
        return data

    def clean_password0(self):
        dataPassword = self.cleaned_data['password0']
        return dataPassword

    def clean_password(self):
        dataPassword = self.cleaned_data['password']
        if 0 < len(dataPassword) and len(dataPassword) < 6:
            raise ValidationError("Password must be longer than 6 symlols")
        return dataPassword
        
    def clean_password2(self):
        dataPassword = self.data['password']
        dataPassword2 = self.cleaned_data['password2']
        if dataPassword != dataPassword2:
            raise ValidationError("Passwords do not match")
        return dataPassword2