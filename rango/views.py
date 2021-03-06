from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Page, UserProfile
from .forms import *
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query

# Create your views here.
def index(request):
	#contruct a dictionary to pass to the template engine as its context
	#Note that the key boldmessage is the same as {{ boldmessage}}
	#context_dict = {'boldmessage' : "I need to do this!"}
	#return a rendered response to send to the client 
	#we make use of the render function to make our lives easier
	#the first argument passed is always the request, followed by the page you wish
	category_list = Category.objects.all()
	page_list = Page.objects.all()
	for category in category_list:
		category.url = category.name.replace(' ', '-')
	context_dict = {'categories':category_list, 'pages':page_list}
	

	
#we access the dictionary list represented by categories by using an object 'category' in html file.
	return render(request, 'rango/index.html', context = context_dict)


#template context simply maps the template variable with the python variables

def about(request):
	context_dict = {'message': "This will be displayed via form or directly via the views. You do not type this in template"}
	
	return render(request, 'rango/about.html', context= context_dict)

#helper function
def get_category_list(max_results = 0, starts_with = ' '):
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__startswith=starts_with)
	else:
		cat_list = Category.objects.all()
	
	if max_results > 0:
		if (len(cat_list) > max_results):
			cat_list = cat_list[:max_results]
	
	for cat in cat_list:
		cat.url = cat.name.replace(' ', '-')
		
	return cat_list


	
"""
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
"""

#we determine which category by using the value passed as parameter category_name_slug
#if the category slug is found in the category() model, we pull out the relevant pages

#REMEMBER : WE USE THE KEY IN THE TEMPLATE

#adding a category. we need something called requestcontext
"""
@csrf_exempt
def add_category(request):
	#get the context from the request
	context = RequestContext(request)
	context_dict = {}

	# a HTTP POST
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		
		#have we been provided with a valid form?
		if form.is_valid():
			form.save(commit=True)
			#not call the index view to show user homepage
			return index(request)
		else:
		#the supplied form contains errors.
		#just print that on the terminal
			print(form.errors)
	else:
		#if the request was not post, display the form to enter details
		form = CategoryForm()
	#bad form. no details supplied
	#render the form with error message
	#context['form'] = form
	return render_to_response('rango/add_category.html',{'form':form},context)
"""
"""
@csrf_exempt
def add_category(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			newcat = form.save(commit=False)
			if len(Category.objects.filter(name=newcat.name))==0:
				newcat.save()
				context_dict["add_success"]="Category"+newcat.name+ " added successfully"
			else:
				context_dict["exists_error"] = "Category already exists"
				print("Category already exists")
		else:
			form = CategoryForm()
		context_dict['form'] = form
	return render_to_response("rango/add_category.html", context_dict, context)
"""
@login_required
def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response("rango/add_category.html", {'form': form}, context)


def show_category(request, category_enc_name):
	context = RequestContext(request)
	category_name = category_enc_name.replace('-',' ')
	context_dict = {"category_enc_name":category_enc_name}
	try:
		cat = Category.objects.get(name=category_name)
		cat.views +=1
		cat.save()
		pages = Page.objects.filter(category=cat).order_by('-views')
		context_dict['pages'] = pages
		context_dict['category'] = cat
		#context_dict['category_enc_name'] = category_enc_name
	except Category.DoesNotExist:
		context_dict['pages'] = None
		context_dict['category'] = None
		#context_dict['category_enc_name'] = category_enc_name
	return render_to_response("rango/category.html", context_dict, context)



"""	
def register(request):
	context = RequestContext(request)
	
	#a boolean vlaue for telling whther the registration was successful or not
	registered = False
	#if its post data, we process the data
	if request.method == "POST":
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		#if the two forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			#now lets sort out the UserProfile instance
			#since we need to set the user attributes ourselves, commit=Flase
			profile = profile_form.save(commit = False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		#invalid form or forms. Mistakes are there
		else:
			print(user_form.errors, profile_form.errors)
			
		#not a HTTP POST, so we render our form using MOdelform instances
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	#render the template depending on the context
	
	return render_to_response("rango/register.html",{'user_form':user_form, 'profile_form':profile_form, 'registered':registered},context)
"""
@csrf_exempt
def register(request):
	#cookies cookies
	if request.session.test_cookie_worked():
		print(">>>TEST COOKIE WORKED!")
		request.sessiom.delete_test_cookie()
	context = RequestContext(request)
	context_dict = {}
#	register_success = True
	
	if request.method=="POST":
		uform = UserForm(request.POST)
		upform = UserProfileForm(request.POST)
		if uform.is_valid() and upform.is_valid():
			user = uform.save(commit=False)
			user.set_password(user.password)
			if user.email=="":
				context_dict["reg_error"]="Email address is required"
			elif User.objects.filter(email=user.email).count() > 0:
				context_dict["reg_error"]="This email address is already in use"
			else:
				user.save()
				uprofile = upform.save(commit = False)
				uprofile.user = user
				if 'picture' in request.FILES:
					uprofile.picture = request.FILES['picture']
				uprofile.save()
				context_dict["reg_success"]="Registration successful"
	else:
		uform = UserForm()
		upform = UserProfileForm()
	context_dict['uform'] = uform
	context_dict['upform'] = upform
	return render_to_response("rango/register.html", context_dict, context)


		
	
@csrf_exempt	
def user_login(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
				
			else:
				return HttpResponse("Your Rango account has been disabled")
		else:
			print("Invalid login details: {0},{1}".format(username, password))
			return HttpResponse("Invalid login details suppiled. Press the back button and go back")
			
	else:
		#no context variable to pass to the template. hence empty
		return render_to_response("rango/login.html",{},context)


def check_logged_in(request):
	if request.user.is_authenticated():
		return HttpResponse("You are logged in")
	else:
		return HttpResponse("you are not logged in")

@login_required
def restricted(request):
	return HttpResponse("Since you're not loggeed in, you can't see this text!")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')

"""
@login_required
def add_page(request, category_enc_name):
	context = RequestContext(request)
	context_dict = {}
	category_name = category_enc_name.replace('-', ' ')
	if request.method == "POST":
		form = PageForm(request.POST)
		if form.is_valid():
			page = form.save(commit = False)
			try:
				cat = Category_objects.get(name=category_name)
				page.category = cat
			except Category.DoesNotExist:
				return render_to_response("rango/add_page.html", context_dict, context)
			page.save()
			return show_categry(request, category_enc_name)
		else:
			print(form.errors)
	else:
		form = PageForm()
	context_dict['category_enc_name'] = category_enc_name
	context_dict['category_name'] = category_name
	context_dict['form'] = form
	
	return render_to_response("rango/add_page.html", context_dict, context)
"""


@login_required
def add_page(request, category_enc_name):
	context = RequestContext(request)
	context_dict = {}
	category_name = category_enc_name.replace('-', ' ')
	context_dict = {"category_enc_name":category_enc_name, "category_name":category_name}
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			page = form.save(commit = False)
			cat = Category.objects.get(name = category_name)
			page.category = cat
			page.views = 0
			page.save()
			return show_category(request, category_enc_name)
		else:
			print(form.errors)
	else:
		form = PageForm()
	context_dict = {"category_enc_name":category_enc_name, "category_name": category_name, "form":form}
	return render_to_response("rango/add_page.html", context_dict, context)

def search(request):
	context = RequestContext(request)
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		
		if query:
			#run the bing function to get the result
			result_list = run_query(query)
		else:
			return HttpResponse("No results found bro.")
	return render_to_response("rango/search.html", {"result_list":result_list}, context)

@login_required
def profile(request):
	context = RequestContext(request)
	cat_list = get_category_list()
	context_dict = {}
	#retrieve the user, then the profile of the user through the user, create a context_dict and pass it to the template. your wish to show the categories or not. i won't7
	u = User.objects.get(username = request.user)
	
	try:
		up = UserProfile.objects.get(user = u)
	except:
		up = None
	context_dict['user'] = u
	context_dict['userprofile'] = up
	return render_to_response("rango/profile.html", context_dict, context)
	

#creating the track of how many times a user visits a page through our website
def track_url(request):
	context = RequestContext(request)
	page_id = None
	#initially we set the id to none. by default we want the url to be the base one. so that it's easier to return a response
	url = '/rango/'
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try:
				page = Page.objects.get(id = page_id)
				page.views = page.views + 1
				page.save()
				url = page.url
			except:
				pass
	return redirect(url)
#this is an example of HTTP GET request. rango/goto/?page_id=1.
