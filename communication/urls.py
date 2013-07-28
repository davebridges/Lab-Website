'''This package has the url encodings for the communication app.'''

from django.conf.urls import patterns, include, url

from communication import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^twitter/?$', views.TwitterView.as_view(), name="twitter"),
    url(r'/?$', views.ContactView.as_view(), name='contact-info'),
)
