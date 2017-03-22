from django.shortcuts import render
from rango.models import Game, Review
from rango.forms import GameForm, ReviewForm, UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
	request.session.set_test_cookie()
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary	
	# that will be passed to the template engine.
	Game_list = Game.objects.order_by('-likes')[:5]
	Review_list = Review.objects.order_by('-views')[:5]
	context_dict = {'categories': Game_list, 'Reviews': Review_list}
	
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

    # Render the response and send it back!
	response = render(request, 'rango/index.html', context_dict)
	return response

def about(request):
	if request.session.test_cookie_worked():
		print("TEST COOKIE WORKED!")
		request.session.delete_test_cookie()
	
	context_dict = {'boldmessage': "This website has been put together by Sean Skilling, Conor Morgan and Thomas Craig."}
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
    # Return a rendered response to the client.
    # We make use of the shortcut function to tmake our lives easier.
    # Note that the first parameter is the template we wish to use.
	return render(request, 'rango/about.html', context = context_dict)

def show_game(request, game_name_slug):
	
	# Create a context dictionary which we can pass
	# to the template rendering engine.
	context_dict = {}
	
	try:
		# Can we find a Game name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception.
		current_game = Game.objects.get(slug=game_name_slug)
		
		# Retrieve all of the associated Reviews.
		# Note that filter() will return a list of Review objects or an empty list
		reviews = Review.objects.filter(game=current_game)
		
		# Adds our results list to the template context under name Reviews
		context_dict['reviews'] = reviews
		# We also add the Game object from
		# teh database to the context dictionary
		# We'll use this in the template to verify that the Game exists
		context_dict['game'] = current_game
		
	except current_game.DoesNotExist:
		# We get here if we didn't find the specified Game
		# Don't do antthing
		# the template will display the "no Game" message for us
		context_dict['game'] = None
		context_dict['reviews'] = None
	# Go render the response and return it to the client
	return render(request, 'rango/game.html', context_dict)
	
def add_game(request):
	form = GameForm()
	
	# A HTTP POST?
	if request.method == 'POST':
		form = GameForm(request.POST)
		
		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new Game to the database.
			form.save(commit=True)
			# Now that the Game is saved
			# We could give a confirmation message
			# But since the most recent Game added is on the index Review
			# Then we can direct the user back to the index Review
			return index(request)
		else:
			# The supplied form contained errors - 
			# just print them to the terminal
			print(form.errors)
			
	# Will handle the bad form, new form or no form supplied cases
	# Render the form with error messages (if any)
	return render(request, 'rango/add_game.html', {'form': form})
	
def add_review(request, game_name_slug):
	try:
		game = Game.objects.get(slug=game_name_slug)
	except Game.DoesNotExist:
		game = None
		
	form = ReviewForm()
	if request.method =='POST':
		form=ReviewForm(request.POST)
		if form.is_valid():
			if game:
				review = form.save(commit=False)
				review.game = game
				review.views = 0
				review.save()
				return show_game(request, game_name_slug)
		else:
			print(form.errors)
			
	context_dict = {'form': form, 'game': game}
	return render(request, 'rango/add_review.html', context_dict)
	
def register(request):
	# A boolean value for telling the template
	# whether the registration was successful
	# Set to False initially. Code changes value to
	# True when registration succeeds
	registered = False
	
	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information
		# Note that we mak use of both UserForm and UserProfileForm
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)
		
		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# # Save the user's form data to the database
			user = user_form.save()
			
			# Now we hash the password with the set_password method
			# Once hashed, we can update the user object
			user.set_password(user.password)
			user.save()
			
			# Now sort out the UserProfile instance
			# Since we need to set the user attribute ourselves
			# we set commit = False. THis delays saving the model
			# until we're ready to avoid integrity problems
			profile = profile_form.save(commit = False)
			profile.user = user
			
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and 
			# put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			
			# Now we save the UserProfile model instance
			profile.save()
			
			# Update our variable to indicate that the template
			# registration was successful
			registered = True
		else:
			# Invalid form or forms - mistakes or something else?
			# Print problems to the terminal
			print(user_form.errors, profile_form.errors)
	else:
		# Not a HTTP POST, so we render our form using two ModelForm instances
		# These forms will be blank, ready for user input
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	# Render the template depending on the context
	return render(request, 'rango/register.html', 
			{'user_form': user_form, 'profile_form': profile_form,
			'registered': registered })
			
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username = username, password = password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your Rango Account is disabled.")
		else:
			print("invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {})
	
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def get_server_side_cookie(request, cookie, default_val = 0):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val
	
def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie(request, 'visits', '1'))
	
	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
	
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		response.set_cookie('last_visit', str(datetime.now()))
	else:
		visits = 1
		request.session['last_visit'] = last_visit_cookie
	request.session['visits'] = visits

