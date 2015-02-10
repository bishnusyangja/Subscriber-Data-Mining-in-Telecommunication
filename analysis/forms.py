from django import forms

Gender = (
	('Male':'Yes'),
	('Female':'No'),
	)
class MyGender(forms.Form):
	gender = forms.ChoiceField(widget=forms.RadioSelect,choices=Gender)