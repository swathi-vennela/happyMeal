from django import forms

class FilterForm(forms.Form):
	filterAtt = forms.CharField(max_length=100, label='Filter Attribute')