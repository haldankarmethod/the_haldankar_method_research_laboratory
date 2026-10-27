from django.contrib import admin
from django.urls import path, include
from the_haldankar_method_research_laboratory import views as proj_views
from haldankar_actual_profit import views as ap_views
from haldankar_aboutme import views as ab_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('haldankar_homepage.urls')),
    path('books/', include('haldankar_book.urls')),
    path('research/', proj_views.research_hub, name='research_hub'),
    path('research/actual-profit/', include('haldankar_actual_profit.urls')),
    path('research/decision-context-model/', include('haldankar_decision_context_model.urls')),
    path('human-information-literacy/', include('HumanInformationLiteracy.urls')),
    path('publications/', proj_views.publications, name='publications'),
    path('laboratory/', ab_views.laboratory, name='laboratory'),
    path('legal/privacy-policy/', ab_views.privacy_policy, name='privacy_policy'),
    path('legal/terms-of-service/', ab_views.terms_of_service, name='terms_of_service'),
    path('evidence/hdfc-experiment/', ap_views.hdfc_experiment, name='hdfc_experiment'),
    path('evidence/white-paper-test/', ap_views.white_paper_test, name='white_paper_test'),
    path('contact/', include('haldankar_contact.urls')),
]
