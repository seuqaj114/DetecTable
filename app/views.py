from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime

def landing(request):
	return render(request,"app/landing.html",{})