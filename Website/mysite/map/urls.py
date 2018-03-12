from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = 'map'
urlpatterns = [
    path('', views.home, name='homepage'),
    path('maps', views.index, name='index'),
    path('overview', views.overview, name='overview'),
    path('contact', views.contact, name='contact'),
    path('references', views.references, name='references'),
    path('methods', views.methods, name='methods'),

]