'''This package has the url encodings for the communication app.'''

from django.urls import path
from communication import views

urlpatterns = [
    path('twitter/', views.TwitterView.as_view(), name="twitter"),
    path('', views.ContactView.as_view(), name='contact-info'),
]
