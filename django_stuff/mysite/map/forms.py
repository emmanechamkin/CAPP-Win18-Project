from django import forms


YEAR_CHOICES = (('1940', '1940'), ('1950', '1950'), 
	('1960', '1960'), ('1970', '1970'), ('1980', '1980'),
	('1990', '1990'), ('2000', '2000'), ('2010','2010'))

IND_CHOICES = (('pa', 'percent aa'), ('seg', 'segregation'), 
	('mhv', 'median home value'), ('pv', 'percent vacant'),
	('pr', 'percent rented'))


class DataForm(forms.Form):
	ind = forms.ChoiceField(
		label = 'Indicator', 
		required = True, 
		choices = IND_CHOICES)
	yr = forms.ChoiceField(
		label = 'Year', 
		required = True, 
		choices = YEAR_CHOICES)


