from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns("",
		url(r'^$',views.landing,name="landing"),
		url(r'^recognize/$',views.recognize,name="recognize"),	
		)