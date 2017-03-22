import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Game, Review

def populate():

	playstation_pages = [
		{"title": "Crash Bandicoot", "views":2},
		{"title": "Castlevania: Symphony of the Night", "views":21},
		{"title": "Spyro", "views":69} ]
	
	xbox_pages = [
		{"title": "Halo 2", "views":34},
		{"title": "The Elder Scrolls III: Morrowind", "views":39},
		{"title": "Halo", "views":-1} ]
	
	n64_pages = [
		{"title": "Super Mario 64", "views":4 },
		{"title": "The Legend of Zelda: Majora's Mask", "views":314} ]
	
	cats = {"Playstation": {"Games": playstation_pages, "views":128, "likes":64},
			"Xbox": {"pages": xbox_pages, "views":64, "likes":32},
			"Nintendo 64": {"pages": n64_pages, "views":32, "likes":16} }
	
	for cat, cat_data in cats.items():
		c=add_cat(cat, cat_data)
		for p in cat_data["pages"]:
			add_review(c, p["title"], p["url"], p["views"])
			
	for c in Game.objects.all():
		for p in Review.objects.filter(category = c):
			print("- {0} - {1}".format(str(c), str(p)))
			
def add_review(cat, title, url, views):
	p = Review.objects.get_or_create(category=cat, title = title)[0]
	p.url = url
	p.views = views
	p.save()
	return p
		
def add_game(name, cat_data):
	c = Game.objects.get_or_create(name=name)[0]
	c.views = cat_data["views"]
	c.likes = cat_data["likes"]
	c.save()
	return c
		
if __name__ == '__main__':
	print ("Starting Rango population script...")
	populate()