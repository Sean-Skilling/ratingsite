from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from django.db import models

class Game(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	developer = models.CharField(max_length = 128)
	platform = models.CharField(max_length=128)
	releaseDate = models.DateField(_("Date"), default=datetime.date.today)
	description = models.CharField(max_length=512)
	views = IntegerField(default = 0)
	image = models.ImageField(upload_to='game_images', blank=True)
	slug = models.SlugField(unique = True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = 'Categories'
	
	def __str__(self):
		return self.name
		
	def __unicode__(self):
		return self.name
		
class Review(models.Model):
	game = models.ForeignKey(Game)
	description = models.CharField(max_length=512)
	rating = models.FloatField(default=0)
	image = models.ImageField(upload_to='review_images', blank=True)


	
	def __str__(self):
		return self.title	
	
	def __unicode__(self):
		return self.title
		
class UserProfile(models.Model):

	user = models.OneToOneField(User)
	

	firstName = models.CharField(max_length = 128)
	surname = models.CharField(max_length = 128)
	

	def __str__(self):
		return self.user.username
	def __unicode__(self):
		return self.user.username