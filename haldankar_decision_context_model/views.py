from django.shortcuts import render

def dcm(request):
    return render(request, 'haldankar_decision_context_model/decision_context_model.html', {
        'active_page': 'research',
        'promo_eligible': True,
    })
