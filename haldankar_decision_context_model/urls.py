from django.urls import path
from . import views

app_name = 'dcm'

urlpatterns = [
    path('', views.dcm, name='dcm'),
]
