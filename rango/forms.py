from django import forms
from rango.models import *
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter category.")
	views=forms.IntegerField(widget=forms.HiddenInput(),initial = 0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	
	class Meta:
		model = Category
		fields = ('name', 'views', 'likes')


class PageForm(forms.ModelForm):
	title= forms.CharField(max_length = 128, help_text="Please enter the title.")
	#category = forms.ForeignKey(Category)
	url = forms.URLField(max_length= 200, help_text="Enter the URL")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	
	class Meta:
		model = Page
		fields = ('title', 'url')

	
class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')
