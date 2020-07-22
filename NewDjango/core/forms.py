from django import forms
from .models import *

class FilterForm(forms.Form):
	filterAtt = forms.CharField(max_length=100, label='Filter Attribute')

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ("comment","rating")

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item 
		fields = ("title","price","discount_price","is_veg" ,"description","calories","image")