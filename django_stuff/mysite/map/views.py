from django.shortcuts import render
from django.http import HttpResponse
from . import forms

# Create your views here.

def index(request):
	return HttpResponse("Maps page to be built")

def home(request):
	context = {}
	result = None
	if request.method == 'GET':
		form = DataForm(request.GET)
		curr_ind = form.ind 
		curr_yr = form.year

	return render(request, 'index.html', context)