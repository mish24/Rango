from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
	#contruct a dictionary to pass to the template engine as its context
	#Note that the key boldmessage is the same as {{ boldmessage}}
	#context_dict = {'boldmessage' : "I need to do this!"}
	#return a rendered response to send to the client 
	#we make use of the render function to make our lives easier
	#the first argument passed is always the request, followed by the page you wish
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories':category_list}
#we access the dictionary list represented by categories by using an object 'category' in html file.
	return render(request, 'rango/index.html', context = context_dict)


#template context simply maps the template variable with the python variables

def about(request):
	context_dict = {'message': "This will be displayed via form or directly via the views. You do not type this in template"}
	return render(request, 'rango/about.html', context= context_dict)

def show_category(request, category_name_slug):
	#create a dictionary which we'll pass to the template rendering engine
	context_dict = {}
	try:
	#we need to find the category name slug with the given name.
	#if that's not possible .get() method raises doesnotexist or returns
	#one model instance
		category = Category.objects.get(slug=category_name_slug)
	#retrive all the associated pages. or return an empty list
		pages = Page.objects.filter(category = category)
		context_dict['pages'] = pages
	#we also add the category object from the database to the dict
	#this is used to verify that the category exists
		context_dict['category']=category
	except Category.DoesNotExist:
		#we come here when we don't find the specified category.
		#don't do anything, display "no category"
		context_dict['category'] = None
		context_dict['pages'] = None
	#go render the response and return it to tclient
	return render(request, 'rango/category.html', context_dict)

#we determine which category by using the value passed as parameter category_name_slug
#if the category slug is found in the category() model, we pull out the relevant pages

#REMEMBER : WE USE THE KEY IN THE TEMPLATE


