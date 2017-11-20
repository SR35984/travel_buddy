from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User
from .models import Trip


def flash_errors(errors, request):
	for error in errors:
		messages.error(request, error)

def current_user(request):
	return User.objects.get(id=request.session['user_id'])

def user(request, id):
	context={
		'user': current_user(request),
	}
	return render(request, 'travel_buddy_app/index.html')

def index(request):
	return render(request, 'travel_buddy_app/index.html')

def register(request):
	if request.method =="POST":
		errors = User.objects.validate_registration(request.POST)

		if not errors:
			user = User.objects.create_user(request.POST)
			request.session['user_id'] = user.id
			return redirect(reverse('dashboard'))

		flash_errors(errors, request)
	return redirect(reverse('landing'))

def login(request):
	if request.method == "POST":
		check = User.objects.validate_login(request.POST)

		if 'user' in check:
			request.session['user_id'] = check['user'].id

			return redirect(reverse('dashboard'))

		flash_errors(check['errors'], request)
	return redirect(reverse('landing'))

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')
	return redirect(reverse('landing'))

def travels(request):
	if 'user_id' not in request.session:
		return redirect('/')

	user = current_user(request)
	context = {
		'user': user,
		'trips': Trip.objects.filter(added_by = user),
		'other_trips': Trip.objects.exclude(added_by = user)
	}
	return render(request, 'travel_buddy_app/dashboard.html', context)

def show_trip(request, trip_id, user_id):
	trip = Trip.objects.get(trip_id = trip_id)
	user = Trip.joined_by.get(user_id = user_id)
	context = {
		'trip': trip
	}
	return render(request, 'travel_buddy_app/dashboard.html', context)

def add_trip(request):
	if request.method == "POST":
		errors = Trip.objects.validate(request.POST)

		if not errors:
			trip = Trip.objects.add_trip(request.POST, request.session["user_id"])
			return redirect(reverse('dashboard'))

		flash_errors(request, errors)
		return redirect(reverse('add_trip'))
	else:
		return render(request, 'travel_buddy_app/add.html')

def join_trip(request, trip_id):
	Trip.objects.join_trip(trip_id, request.session["user_id"])
	return redirect(reverse('dashboard'))