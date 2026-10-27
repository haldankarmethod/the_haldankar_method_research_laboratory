from django.shortcuts import render

def foundation_view(request):
    """
    Renders the isolated Educational Foundation Webpage for Human Information Literacy
    and White Paper Test Theory.
    """
    return render(request, 'HumanInformationLiteracy/foundation.html')

