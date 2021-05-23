from django.db import models
import bcrypt
from datetime import date, datetime
from time import strptime
import re


# Create your models here.
class RegistrationManager(models.Manager):
	@staticmethod
	def basic_validator(post_data):
		"""validator for name, email, pw
		all key names come from form in index.html"""
		errors = {}
		if len(post_data['first_name']) < 3:
			errors["first_name"] = "Name should be at least 3 characters"
		if not post_data['last_name'].isalpha():
			errors["first_name"] = "Name should only be alphabetical characters"

		if len(post_data['last_name']) < 3:
			errors["last_name"] = "Name should be at least 3 characters"
		if not post_data['last_name'].isalpha():
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

		if len(post_data['email']) < 6:
			errors['email'] = "Email is too short, 6 or more characters"

		if len(post_data['password']) < 10:
			errors['password'] = "Password is too short, 15 or more characters please"

		if post_data['password'] != post_data['confirm_password']:
			errors['match'] = "Password does not match password confirmation"

		if datetime.strptime(post_data['birthday'], '%Y/%m/%d') > datetime.today():
			errors['birthday'] = 'Birthdate must be in the past, cannot be a future time'
		return errors

	def auth(self, form):
		"""authenticate user"""
		users_with_email = self.filter(email=email)
		if users_with_email:
			current_user = users_with_email[0]
			if bcrypt.hashpw(form['password'].current_user.encode()):
				return True
			else:
				return False
		return False
		# return bcrypt.hashpw(form['password'].current_user.encode())

	def register(self, form):
		"""to use in views for registration"""
		password_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
		return self.create(
			first_name=form['first_name'],
			last_name=form['last_name'],
			birthday=form['birthday'],
			email=form['email'],
			password=password_hash,
		)


class Registration(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	birthday = models.CharField(max_length=20, default='birthday')
	email = models.CharField(max_length=20)
	password = models.CharField(default='password',
								max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = RegistrationManager()


