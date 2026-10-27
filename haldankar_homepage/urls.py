from django.urls import path
from . import views

app_name = 'haldankar_homepage'

urlpatterns = [
    path('', views.home, name='home'),
]
