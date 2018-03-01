from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from . import forms
from . import genquery


# Create your views here.

#def index(request):
#	return HttpResponse("Maps page to be built")

def index(request):
	args = {}
	if request.method == 'GET':
		form = forms.DataForm(request.GET)
		if form.is_valid():
			if form.cleaned_data['ind']:
				args['ind'] = form.cleaned_data['ind']
			if form.cleaned_data['yr']:
				args['yr'] = form.cleaned_data['yr']
			
			# feed args to script here
#			map_info = genquery = run_query(args)


	return render(request, 'index.html', {'form': form})