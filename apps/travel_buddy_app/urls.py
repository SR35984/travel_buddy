from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name="landing"),
	url(r'register$', views.register, name="register"),
	url(r'login$', views.login, name="login"),
	url(r'travels$', views.travels, name="dashboard"),
	url(r'logout$', views.logout, name="logout"),
	url(r'^travels/destination/(?P<trip_id>\d+)/$', views.show_trip, name="show_trip"),
	url(r'travels/add$', views.add_trip, name="add_trip"),
	url(r'^join/(?P<trip_id>\d+)/$', views.join_trip, name="join_trip")
]
