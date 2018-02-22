from django.db import models

# Create your models here.
class Option(models.NullBooleanField):
	public = models.NullBooleanField(default=None)