from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
	return render(request, "index.html")

# def register(request, id):
# 	errors = Registration.objects.basic_validator(request.POST)
#
# 	if len(errors) > 0:
# 		for key, value in errors.items():
# 			messages.error(request, value)
# 		return redirect('/registration/' + id)
# 	else:
# 		reg = Registration.objects.get(id=id)
# 		reg.name = request.POST['first_name']
# 		reg.desc = request.POST['last_name']
# 		reg = request.POST['email']
# 		reg.save()
# 		return redirect('/registration')

def register(request):
	if request.method == 'POST':
		# Registration form
		errors = Registration.objects.basic_validator(request.POST)
		# errors = User.objects.registration_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
				# messages.error(request, error, extra_tags=tag)
			return redirect('/')
		else:
			# Create User
			# password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
			# password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode('utf-8')
			user = Registration.objects.register(request.POST)
			# user = Registration.objects.create(
			# 	first_name=request.POST['first_name'],
			# 	last_name=request.POST['last_name'],
			# 	email=request.POST['email'],
			# 	password=password_hash)
			request.session['user_id'] = user.id
			return redirect('/success')
			# request.session['success'] = "registered"
	# return redirect('/success')

def success(request):
	"""GET request
	"""
	# user = Registration.objects.create(first_name=request.POST['first_name'],
	# last_name=request.POST['last_name'], email=request.POST['email'])
	# request.session['user_id'] = user.id
	# tried doing if == 'POST'
	context = {
		'logged_in_user': Registration.objects.get(id=request.session['user_id'])
	}
	return render(request, 'success_landing.html', context)


def login(request):
	"""user login check
	password hash check from db and from form
	"""
	if request.method == "POST":
		users_with_email = Registration.objects.filter(
			email=request.POST['email'])
		# truthy statement, list with items will be true
		if users_with_email:
			logged_in = users_with_email[0]
			# if password hash inputted = password hash in db
			if bcrypt.checkpw(request.POST['password'].encode(), logged_in.password.encode()):
				# store session for ind user
				request.session['user_id'] = logged_in.id
				return redirect('/success')
			else:
				messages.error(request, "Either Email or password are not correct")
			return redirect('/')

def logout(request):
	# logout session
	request.session.flush()
	return redirect('/')


