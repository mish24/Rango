from django.db import models
from django.template.defaultfilters import slugify
import uuid

# Create your models here.
#a category has a name, number of likes and number of visits
#a page has a category reference, title, url and number of views

class Category(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	views = models.IntegerField(default = 0)
	likes = models.IntegerField(default = 0)
	slug = models.SlugField(unique = True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name_plural = 'Categories'
		

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length = 128)
	url = models.URLField()
	views = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.title

