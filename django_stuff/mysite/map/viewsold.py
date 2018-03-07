from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from . import forms
from . import genquery
import json
from django.core.serializers import serialize
from django.template.loader import get_template


filename = 'data/census_all_final2.geojson'

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

	#geojson['type'] = data['type']
	#geojson['crs'] = data['crs']
	geojson = []	

	for feature in data['features']:
		if feature['properties']['year'] == year:
			geojson.append(feature)
			#for coord in feature['geometry']['coordinates'][0]:
			#geojson.append(coord)
			
	#json.dumps(geojson)
	##if data[feature]
	#geojson_geo = serialize('geojson', geojson, geometry_field = 'geometry')
	#print(json.dumps(geojson))
	response = json.dumps(geojson)
	print(response)
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
	args = {}
	if request.method == 'GET':
		cf = forms.ContactForm()
	if request.method == 'POST':
		cf = forms.ContactForm(request.POST)
		if cf.is_valid():
			e = request.POST.get('email', '')
			m = request.POST.get('message', '')
			tem = get_template('contact.txt')
			c = {
				'em' : e,
				'message' : m
				}
			s = tem.render(c)

			email = EmailMessage(
				"Contact form submission", 
				s, "HOLC site", ['enechamkin@uchicago.edu'],
				headers = {'Reply-To': e})
			email.send()
			# go back to the home page
			messages.success(request, 'Your email has been sent')
			return render(request, 'homepage.html', {})
	return render(request, 'contact.html', {'form' : cf})


