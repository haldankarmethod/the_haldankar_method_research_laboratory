from django.shortcuts import render

def home(request):
    return render(request, 'haldankar_homepage/home.html', {
        'active_page': 'home',
        'promo_eligible': True,
    })
