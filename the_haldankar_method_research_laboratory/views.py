from django.shortcuts import render

def research_hub(request):
    return render(request, 'research_hub.html', {
        'active_page': 'research',
        'promo_eligible': True,
    })

def publications(request):
    return render(request, 'publications.html', {
        'active_page': 'publications',
        'promo_eligible': True,
    })
