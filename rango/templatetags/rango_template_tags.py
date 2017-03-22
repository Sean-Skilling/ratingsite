from django import template
from rango.models import Game

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_game_list(cat = None):
	return {'cats': Game.objects.all(), 'act_cat': cat}