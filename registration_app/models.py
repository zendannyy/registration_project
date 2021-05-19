from django.db import models
import re

# Create your models here.
class RegistrationManager(models.Manager):
	def basic_validator(self, post_data):
		"""validator for name, email, pw
		all key names come from form in index.html"""
		errors = {}
		if len(post_data.get('first_name')) < 3:
			errors["first_name"] = "Name should be at least 3 characters"
		if not post_data.get('last_name').isalpha():
			errors["first_name"] = "Name should only be alphabetical characters"

		if len(post_data.get('last_name')) < 3:
			errors["last_name"] = "Name should be at least 3 characters"
		if not post_data.get('last_name').isalpha():
			errors["first_name"] = "Name should only be alphabetical characters"

		email_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
		if not email_re.match(post_data['email']):
			errors['email'] = "Invalid email address"

		# using email from Registration class in filter method
		# for unique validation of emails, using filer since this can contain empty lists and won't break
		users_with_email = Registration.objects.filter(
			email=post_data['email'])
		if len(users_with_email) >= 1:
			errors['dupe'] = "Email is taken, choose another"

		if len(post_data['password']) < 10:
			errors['password'] = "Password is too short, 15 or more characters please"

		if post_data['password'] != post_data['confirm_password']:
			errors['match'] = "Password does not match password confirmation"
		return errors

	def auth(self, email, password):
		"""authenticate user"""
		users_with_email = self.filter(email=email)
		if not user:
			return False
		user_with_email = users_with_email[0]
		return bcrypt.hashpw(request.POST['password'].user_with_email.encode())

	def register(self, form):
		"""to use in views for registration"""
		password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
		return self.create(
			first_name=request.POST['first_name'],
			last_name=request.POST['last_name'],
			email=request.POST['email'],
			password=password_hash,
		)

class Registration(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.CharField(max_length=20)
	password = models.CharField(default='password',
								max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = RegistrationManager()


