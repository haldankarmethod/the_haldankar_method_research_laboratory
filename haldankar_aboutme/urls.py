from django.urls import path
from . import views

app_name = 'aboutme'

urlpatterns = [
    path('', views.laboratory, name='laboratory'),
    path('legal/privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('legal/terms-of-service/', views.terms_of_service, name='terms_of_service'),
]
