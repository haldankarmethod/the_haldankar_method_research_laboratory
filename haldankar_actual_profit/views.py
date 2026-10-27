from django.shortcuts import render

def index(request):
    return render(request, 'haldankar_actual_profit/index.html', {
        'active_page': 'research',
        'monograph_active': 'index',
        'promo_eligible': True,
    })

def chapter_01(request):
    return render(request, 'haldankar_actual_profit/chapter_01.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_01',
        'promo_eligible': True,
    })

def chapter_02(request):
    return render(request, 'haldankar_actual_profit/chapter_02.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_02',
        'promo_eligible': True,
    })

def chapter_03(request):
    return render(request, 'haldankar_actual_profit/chapter_03.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_03',
        'promo_eligible': True,
    })

def chapter_04(request):
    return render(request, 'haldankar_actual_profit/chapter_04.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_04',
        'promo_eligible': True,
    })

def chapter_05(request):
    return render(request, 'haldankar_actual_profit/chapter_05.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_05',
        'promo_eligible': True,
    })

def chapter_06(request):
    return render(request, 'haldankar_actual_profit/chapter_06.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_06',
        'promo_eligible': True,
    })

def chapter_07(request):
    return render(request, 'haldankar_actual_profit/chapter_07.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_07',
        'promo_eligible': True,
    })

def chapter_08(request):
    return render(request, 'haldankar_actual_profit/chapter_08.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_08',
        'promo_eligible': True,
    })

def chapter_09(request):
    return render(request, 'haldankar_actual_profit/chapter_09.html', {
        'active_page': 'research',
        'monograph_active': 'chapter_09',
        'promo_eligible': True,
    })

def who_should_read(request):
    return render(request, 'haldankar_actual_profit/who_should_read.html', {
        'active_page': 'research',
        'monograph_active': 'who_should_read',
        'promo_eligible': True,
    })

def legal_notice(request):
    return render(request, 'haldankar_actual_profit/legal_notice.html', {
        'active_page': 'research',
        'monograph_active': 'legal_notice',
        'promo_eligible': True,
    })

def hdfc_experiment(request):
    return render(request, 'haldankar_actual_profit/hdfc_experiment.html', {
        'active_page': 'evidence',
        'promo_eligible': True,
    })

def white_paper_test(request):
    return render(request, 'haldankar_actual_profit/white_paper_test.html', {
        'active_page': 'evidence',
        'promo_eligible': True,
    })
