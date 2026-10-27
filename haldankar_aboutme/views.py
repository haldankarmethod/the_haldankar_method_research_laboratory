from django.shortcuts import render

def laboratory(request):
    return render(request, 'haldankar_aboutme/laboratory.html', {
        'active_page': 'laboratory',
        'promo_eligible': True,
    })

def privacy_policy(request):
    return render(request, 'haldankar_aboutme/privacy_policy.html', {
        'active_page': 'legal',
        'promo_eligible': True,
    })

def terms_of_service(request):
    return render(request, 'haldankar_aboutme/terms_of_service.html', {
        'active_page': 'legal',
        'promo_eligible': True,
    })
