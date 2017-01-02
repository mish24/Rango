from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
#Do this properly. it will help in the gsoc project as well. 
#do not cheat. 
#research everything properly else you it will never help you
#PLEASE PLEASE PLEASE DO THIS ON YOUR OWN AND REVISE

class IndexPageTests(TestCase):
	
	def test_index_contains_hello_message(self):
		#check if there is a message 'rango says'
		response = self.client.get(reverse('index'))
		self.assertIn(b'Rango says', response.content)
		
	def test_index_using_template(self):
		#check the template used to render index page
		response = self.client.get(reverse('index'))
		self.assertTemplateUsed(response, 'rango/index.html')
		
	def test_index_has_title(self):
		#check to make sure that tile tag has been used
		response = self.client.get(reverse('index'))
		self.assertIn(b'<title>', response.content)
		
class AboutPageTests(TestCase):


	def test_about_contains_my_name(self):
		response = self.client.get(reverse('about'))
		self.assertIn(b'Poonam', response.content)
		
	def test_about_using_template(self):
		response = self.client.get(reverse('about'))
		self.assertTemplateUsed(response, 'rango/about.html')
		
	def test_about_contains_image(self):
		response = self.client.get(reverse('about'))
		self.assertIn(b'img', response.content)
		
#now lets make the tests for the models
class ModelTests(TestCase):
	
	def setUp(self):
		try:
			from populate_rango import populate
			populate()
		except ImportError:
			print('The module populate_range does not exist')
		except NameError:
			print('Some other name is used')
		except:
			print('Some other error is there i have a headache :(')
			
	def get_category(self, name):
		from rango.models import Category
		try:
			cat = Category.objects.get(name = name)
		except Category.DoesNotExist:
			cat = None
		return cat
		
	def test_python_cat_added(self):
		cat = self.get_category('Python')
		self.assertIsNotNone(cat)
	
	
		
	
		
		


