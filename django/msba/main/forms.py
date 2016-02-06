from django import forms

class signup_form(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=8, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm password', max_length=8, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')

