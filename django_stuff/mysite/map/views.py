from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from . import forms
from . import genquery
import json

filename = '../'

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
				cx['data'] = process_data(filename, form.cleaned_data['yr'])
	
	# Build remaining context
	cx['form'] = form
	cx['args'] = args

	return render(request, 'index.html', cx)

def process_data(filename, year):
	'''
	process the rows of the file
	'''
	geojson = {}

	with open(filename) as f:
		data = json.load(f)

	geojson['type'] = data['type']
	geojson['crs'] = data['crs']
	geojson['features'] = []	

	for feature in data['features']:
		if feature['properties']['year'] == year:
			geojson['features'].append(feature)

	json.dumps

	return geojson

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


