import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

	playstation_pages = [
		{"title": "Crash Bandicoot",
		"url":"http://docs.python.org/2/tutorial/", "views":2},
		{"title": "Castlevania: Symphony of the Night",
		"url":"http://www.greenteapress.com/thinkpython/", "views":21},
		{"title": "Spyro",
		"url":"http://www.korokithakis.net/tutorials/python/", "views":69} ]
	
	xbox_pages = [
		{"title": "Halo 2",
		"url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/", "views":34},
		{"title": "The Elder Scrolls III: Morrowind",
		"url":"http://www.djangorocks.com/", "views":39},
		{"title": "Halo",
		"url":"http://www.tangowithdjango.com/", "views":-1} ]
	
	n64_pages = [
		{"title": "Super Mario 64",
		"url":"http://bottlepy.org/docs/dev/", "views":4 },
		{"title": "The Legend of Zelda: Majora's Mask",
		"url":"http://www.flask.pocoo.org", "views":314} ]
	
	cats = {"Playstation": {"pages": playstation_pages, "views":128, "likes":64},
			"Xbox": {"pages": xbox_pages, "views":64, "likes":32},
			"Nintendo 64": {"pages": n64_pages, "views":32, "likes":16} }
	
	for cat, cat_data in cats.items():
		c=add_cat(cat, cat_data)
		for p in cat_data["pages"]:
			add_page(c, p["title"], p["url"], p["views"])
			
	for c in Category.objects.all():
		for p in Page.objects.filter(category = c):
			print("- {0} - {1}".format(str(c), str(p)))
			
def add_page(cat, title, url, views):
	p = Page.objects.get_or_create(category=cat, title = title)[0]
	p.url = url
	p.views = views
	p.save()
	return p
		
def add_cat(name, cat_data):
	c = Category.objects.get_or_create(name=name)[0]
	c.views = cat_data["views"]
	c.likes = cat_data["likes"]
	c.save()
	return c
		
if __name__ == '__main__':
	print ("Starting Rango population script...")
	populate()