from django.shortcuts import render

def books_hub(request):
    return render(request, 'haldankar_book/architecture_of_a_decision.html', {
        'active_page': 'books',
        'promo_eligible': True,
    })
