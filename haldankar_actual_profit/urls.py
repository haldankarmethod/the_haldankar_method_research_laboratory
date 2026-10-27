from django.urls import path
from . import views

app_name = 'actual_profit'

urlpatterns = [
    path('', views.index, name='index'),
    path('chapter-01-system-architecture/', views.chapter_01, name='chapter_01'),
    path('chapter-02-human-processor/', views.chapter_02, name='chapter_02'),
    path('chapter-03-screen/', views.chapter_03, name='chapter_03'),
    path('chapter-04-white-paper-test/', views.chapter_04, name='chapter_04'),
    path('chapter-05-applied-case-studies/', views.chapter_05, name='chapter_05'),
    path('chapter-06-decision-integrity/', views.chapter_06, name='chapter_06'),
    path('chapter-07-dimensionality/', views.chapter_07, name='chapter_07'),
    path('chapter-08-advanced-algorithm/', views.chapter_08, name='chapter_08'),
    path('chapter-09-closing-perspective/', views.chapter_09, name='chapter_09'),
    path('who-should-read/', views.who_should_read, name='who_should_read'),
    path('legal-notice/', views.legal_notice, name='legal_notice'),
    path('evidence/hdfc-experiment/', views.hdfc_experiment, name='hdfc_experiment'),
    path('evidence/white-paper-test/', views.white_paper_test, name='white_paper_test'),
]
