from django import forms

from . import validations

class LoginForm(forms.Form):
    name=forms.CharField(min_length=1, max_length=50)
    password=forms.CharField(
        min_length=1
      , max_length=30
      , widget=forms.PasswordInput
    )

class PhoneForm(forms.Form):
    phone=forms.CharField(
        min_length=9
      , max_length=10
      , validators=[validations.validate_phone_number]
    )
