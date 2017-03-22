from django import forms
from rango.models import Review, Game, UserProfile
from django.contrib.auth.models import User

class GameForm(forms.ModelForm):

	class Meta:
		model = Game
		exclude = ('slug', 'views' )
	
class ReviewForm(forms.ModelForm):
	class Meta:

		model = Review
		fields = ('game', 'description', 'rating', 'image' )


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('firstName', 'surname')