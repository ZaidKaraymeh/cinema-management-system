from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import User



class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    birth = forms.DateField(
        label='', widget=forms.SelectDateWidget(years=range(2012, 1950, -1)))
    class Meta:
        # Interacts with User model
        model = User
        # What fields to show and in which order
        fields = ["first_name", "last_name", "email",
                  "password1", "password2", "user_type", 
                "birth", "phone_number"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

"""
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
"""
