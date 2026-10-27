from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('submit/', views.submit_inquiry, name='submit'),
    path('cirf/', views.cirf_inquiry, name='cirf_inquiry'),
    path('cirf/submit/', views.submit_cirf_inquiry, name='submit_cirf_inquiry'),
]
