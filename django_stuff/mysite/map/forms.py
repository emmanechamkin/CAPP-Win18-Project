from django import forms

# ["Total_Pop", "PCT_WHITE", "PCT_BLACK", "PCT_OTHER", 
# "TOTAL_UNITS", "Median", "PCT_OCCUPIED", "PCT_VACANT", "PCT_OWN_OCC", "PCT_RENT_OCC"]

YEAR_CHOICES = (('1940', '1940'), ('1950', '1950'), 
	('1960', '1960'), ('1970', '1970'), ('1980', '1980'),
	('1990', '1990'), ('2000', '2000'), ('2010','2010'))

IND_CHOICES = (('PCT_WHITE', 'Percent white'), ('PCT_BLACK', 'Percent black'), 
	('norm_med', 'Normalized median home value'), ('PCT_VACANT', 'Percent vacant'),
	('PCT_RENT_OCC', 'Percent renter occupied'), ('PCT_OWN_OCC', 'Percent owner occupied'))


class DataForm(forms.Form):
	ind = forms.ChoiceField(
		label = 'Indicator', 
		required = True, 
		choices = IND_CHOICES)
	yr = forms.ChoiceField(
		label = 'Year', 
		required = True, 
		choices = YEAR_CHOICES)
	tog = forms.BooleanField(
		label= 'Toggle on redline boundaries')

class ContactForm(forms.Form):
	email = forms.EmailField(required=True)
	messsage = forms.CharField(
		required=True,
		widget=forms.Textarea)

	#def __init__(self, *args, **kwargs):
	#	super(ContactForm, self).__init__(*args, **kwargs)
	#		self.fields['email'].help_text = "example@foo.bar"
	#	self.fields['message'].help_text = "what would you like to share" 

