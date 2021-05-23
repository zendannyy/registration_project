from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


# Create your views here.
def index(request):
	if request == 'POST':
		return redirect('/')
	else:
		return render(request, "index.html")


def success(request):
	"""GET request
	"""
	# tried doing if == 'POST'
	# context = {
	# 	'logged_in_user': Registration.objects.get(id=request.session['user_id'])
	# }
	if request.session['user_id']:
		return render(request, 'success_landing.html',
					  {"user": Registration.objects.get(
						  id=request.session['user_id'])})
	else:
		return redirect('/')
# return render(request, 'success_landing.html', context)


def register(request):
	if request.method == 'POST':
		# Registration form
		errors = Registration.objects.basic_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		else:
			# Create User
			user = Registration.objects.register(request.POST)
			request.session['user_id'] = user.id
			return redirect('/dashboard')

	return redirect('/success')


def login(request):
	"""user login check
	password hash check from db and from form
	"""
	if request.method == "POST":
		users_with_email = Registration.objects.filter(
			email=request.POST['email'])
		# truthy statement, list with items will be true
		print('Above if')
		if users_with_email:
			logged_in = users_with_email[0]
			# if password hash inputted = password hash in db # tried .encode('utf-8')
			if bcrypt.checkpw(request.POST['password'].encode(), logged_in.password.encode()):
				# store session for ind user
				request.session['user_id'] = logged_in.id
				request.session['first_name'] = logged_in.first_name
				return redirect('/dashboard')
			else:
				messages.error(request, "Either Email or password are not correct")

	return redirect('/')


def logout(request):
	# logout session
	request.session.flush()
	return redirect('/')
