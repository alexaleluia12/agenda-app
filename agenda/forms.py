from django import forms


class LoginForm(forms.Form):
    name=forms.CharField(min_length=1, max_length=50)
    password=forms.CharField(min_length=1, max_length=30, widget=forms.PasswordInput)


