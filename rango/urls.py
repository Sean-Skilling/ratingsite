from django.conf.urls import url
from rango import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^about/', views.about, name = 'about'),
	url(r'^add_game/$', views.add_game, name='add_game'),
	url(r'^game/(?P<game_name_slug>[\w\-]+)/$',
		views.show_game, name='show_game'),
	url(r'^game/(?P<game_name_slug>[\w\-]+)/add_review/$',
		views.add_review, name='add_review'),
	url(r'^register/$', views.register, name = 'register'), # New pattern!
	url(r'^login/$', views.user_login, name = 'login'),
	url(r'^restricted/', views.restricted, name = 'restricted'),
	url(r'^logout/$', views.user_logout, name = 'logout'),
	url(r'^profile/$', views.user_profile, name = 'profile'),
	
]