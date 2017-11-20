from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
	def validate_registration(self, form_data):
		errors =[]
		name = form_data['name']
		username = form_data['username']
		password = form_data['password']
		confirmation_password = form_data['password_confirmation']

		if len(name) == 0:
			errors.append("Name is required!")
		if len(name) < 3:
			errors.append("Name must be at least 3 characters long!")

		if len(username) == 0:
			errors.append("Username is required!")
		if len(username) < 3:
			errors.append("Username must be at least 3 characters long!")

		if len(password) == 0:
			errors.append("Password is required!")
		if len(password) < 8:
			errors.append("Password must be at least 8 characters long!")
		elif password != confirmation_password:
			errors.append("Passwords must match!")

		if not errors:
			user_list = self.filter(username=username)
			if user_list:
				errors.append('Username already taken!')

		return errors

	def validate_login(self, form_data):
		errors = []
		username = form_data['username']
		password = form_data['password']
		
		if len(username) == 0:
			errors.append("Username is required!")
		
		if len(password) == 0:
			errors.append("Password is required!")

		if not errors:
			user_list = User.objects.filter(username=username)

			if user_list:
				user = user_list[0]
				user_password = password.encode()
				db_password = user.password.encode()

				if bcrypt.checkpw(user_password, db_password):
					return {'user': user}

		errors.append("Username or Password invalid")

		return {'errors': errors}

	def create_user(self, form_data):
		password = form_data['password']
		hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

		return User.objects.create(
			name = form_data['name'],
			username = form_data['username'],
			password = hashedpw,
	)

class User(models.Model):
	name = models.CharField(max_length=45)
	username = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class TripManager(models.Manager):
	def validate(self, form_data):
		errors = []
		destination = form_data['destination']
		description = form_data['description']
		travel_date_from = form_data['travel_date_from']
		travel_date_to = form_data['travel_date_to']

		if len(destination) == 0:
			errors.append("Please type a Destination!")
		if len(description) == 0:
			errors.append("Please type a Description!")
		if len(travel_date_from) == 0:
			errors.append("Please type a Date From! Trips should be future dates!")
		if len(travel_date_to) == 0:
			errors.append("Please type a Date To! Date To should be after Date From!")

		return errors

	def add_trip(self, form_data, user_id):
		user = User.objects.get(id=user_id)
		trip = self.create(
		destination = form_data['destination'],
		description = form_data['description'],
		travel_date_from = form_data['travel_date_from'],
		travel_date_to = form_data['travel_date_to'],
		added_by = user
		)
		return trip

	def join_trip(self, trip_id, user_id):
		user = User.objects.get(id=user_id)
		trip = Trip.objects.get(id=trip_id)
		user.joined.add(trip)

class Trip(models.Model):
	destination = models.CharField(max_length=45)
	description = models.CharField(max_length=45)
	travel_date_from = models.CharField(max_length=45)
	travel_date_to = models.CharField(max_length=45)
	added_by = models.ForeignKey(User, related_name="added_trips")
	joined_by = models.ManyToManyField(User, related_name="joined")
	objects = TripManager()