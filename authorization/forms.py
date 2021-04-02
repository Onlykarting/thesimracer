from django import forms


class LoggingInForm(forms.Form):
    username = forms.CharField(label='Login', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())
    logging = forms.CharField(label='logging', required=False)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())
    register = forms.CharField(label='logging', required=False)
