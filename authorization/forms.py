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


class ProfileDataForm(forms.Form):
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    discord = forms.CharField(label='Discord', required=True, max_length=20)
    twitch = forms.CharField(label='Twitch', required=True, max_length=20)
    instagram = forms.CharField(label='Instagram', required=True, max_length=20)
    country_name = forms.CharField(widget=forms.Select, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True, max_length=500)
    tag = forms.CharField(label='Tag', required=True, max_length=3, min_length=3)
