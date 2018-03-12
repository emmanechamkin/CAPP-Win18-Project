from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from . import forms
from . import genquery
import json


filename = 'data/census_all_final6.geojson'

# Create your views here.
def index(request):
	args = {}
	cx = {}
	if request.method == 'GET':
		form = forms.DataForm()
	if request.method == 'POST':
		form = forms.DataForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['ind']:
				args['ind'] = form.cleaned_data['ind']
			if form.cleaned_data['yr']:
				args['yr'] = form.cleaned_data['yr']
				cx['data'] = process_data(filename, int(form.cleaned_data['yr']))
	
	# Build remaining context
	cx['form'] = form
	cx['args'] = json.dumps(args)

	return render(request, 'index.html', cx)

def process_data(filename, year):
	'''
	process the rows of the file
	'''
	with open(filename) as f:
		data = json.load(f)

	geojson = []	

	for feature in data['features']:
		if feature['properties']['year'] == year:
			geojson.append(feature)

	response = json.dumps(geojson)

	return response

def home(request):
	return render(request, 'homepage.html', {})

def overview(request):
	return render(request, 'overview.html', {})

def methods(request):
	return render(request, 'methods.html', {})

def references(request):
	return render(request, 'reference.html', {})

def contact(request):
	return render(request, 'contact.html', {})


