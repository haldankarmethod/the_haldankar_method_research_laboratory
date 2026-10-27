from django.urls import path
from . import views

app_name = 'human_information_literacy'

urlpatterns = [
    path('foundation/', views.foundation_view, name='foundation'),
]
