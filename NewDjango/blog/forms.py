from django import forms
from django.contrib.auth.models import User
from . models import *


class ContactUsForm(forms.ModelForm):

    class Meta():
        model = ContactUs
        fields = '__all__'
