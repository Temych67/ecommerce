from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Account
from django.contrib.auth import authenticate
from store.models import Customer
from django.contrib.auth.forms import UserChangeForm

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "example@gmail.com",
                # "value"       : "test",
                "class"       : "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                # "value"       : "ApS12_ZZs8",                
                "class"       : "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "First name",                
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Last name",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = Account
        fields = ('first_name','last_name', 'email', 'password1', 'password2')
				

class AccountUpdateForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('email','first_name','last_name')

    def cleaned_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is alredy in use.' % email)

    def cleaned_first_name(self):
        first_name = self.cleaned_data['first_name']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(first_name=first_name)
        except Account.DoesNotExist:
            return first_name
    def cleaned_last_name(self):
        last_name = self.cleaned_data['last_name']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(last_name=last_name)
        except Account.DoesNotExist:
            return last_name
