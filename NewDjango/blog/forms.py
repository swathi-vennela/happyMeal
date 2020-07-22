from django import forms
from django.contrib.auth.models import User
from . models import *


class ContactUsForm(forms.ModelForm):

    class Meta():
        model = ContactUs
        fields = ['message', 'name', 'email']

        def __init__(self, *args, **kwargs):
	        super(ContactUsForm, self).__init__(*args, **kwargs)
	        self.fields['message'].widget = forms.TextInput(
	            attrs={ 'placeholder': 'Your message'})
	        self.fields['message'].label = False
	        self.fields['name'].widget = forms.TextInput(
	            attrs={ 'placeholder': 'Your name'})
	        self.fields['name'].label = False
	        self.fields['email'].widget = forms.TextInput(
	            attrs={ 'placeholder': 'Your email'})
	        self.fields['email'].label = False