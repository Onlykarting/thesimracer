from django import forms

class LoggingInForm(forms.Form):
    login = forms.CharField(label='Login', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())
