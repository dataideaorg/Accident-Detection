from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    date_of_birth = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1900, 2100)))
    organization = forms.CharField(max_length=100, required=False)
    occupation = forms.CharField(max_length=100, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'organization', 'occupation', 'password1', 'password2')



User = get_user_model()

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')