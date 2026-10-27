from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('the-architecture-of-a-decision/', views.books_hub, name='books_hub'),
]
