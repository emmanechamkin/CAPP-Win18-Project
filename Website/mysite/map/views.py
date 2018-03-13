from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from . import forms
import json


filename = 'data/census_all_final.geojson'

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
				# Filter the data using year value returned from form
				cx['data'] = process_data(filename,int(form.cleaned_data['yr']))
			if form.cleaned_data['tog']:
				args['tog'] = form.cleaned_data['tog']
	
	# Build remaining context
	cx['form'] = form
	cx['args'] = json.dumps(args)

	return render(request, 'index.html', cx)

def process_data(filename, year):
	'''
	Filter a GeoJSON file using on year and return a GeoJSON readable object

	Inputs:
		filename (str): directs to location of full GeoJSON file within the 
			Django infrastructure
		year (int): Year of interest, can only be a decade between 1940 and 2010
			as returned by the form

	Returns filtered GeoJSON object to read into Leaflet Javascript application
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


