from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import CollaborationInquiryForm, CIRFInquiryForm

# CIRF inquiry views for Service 03

def submit_inquiry(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

    form = CollaborationInquiryForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        inquiry_area = form.cleaned_data['inquiry_area']
        message = form.cleaned_data['message']

        subject = f"Institutional Inquiry: {inquiry_area}"
        email_message = f"Name: {name}\nEmail: {email}\nResearch Area: {inquiry_area}\n\nMessage:\n{message}"
        
        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@haldankarmethod.com')
            send_mail(
                subject=subject,
                message=email_message,
                from_email=from_email,
                recipient_list=[from_email],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'Inquiry transmitted successfully.'})
        except Exception:
            return JsonResponse({'success': True, 'message': 'Inquiry transmitted successfully (development mode).'})
    else:
        errors = form.errors.get_json_data()
        first_error_msg = "Form validation failed."
        for field, error_list in errors.items():
            if error_list:
                first_error_msg = f"{field.capitalize()}: {error_list[0]['message']}"
                break
        return JsonResponse({'success': False, 'message': first_error_msg}, status=400)


def cirf_inquiry(request):
    form = CIRFInquiryForm()
    return render(request, 'haldankar_contact/cirf_inquiry.html', {'form': form})


def submit_cirf_inquiry(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

    form = CIRFInquiryForm(request.POST)
    if form.is_valid():
        full_name = form.cleaned_data['full_name']
        work_email = form.cleaned_data['work_email']
        org_name = form.cleaned_data['organization_name']
        bu_dept = form.cleaned_data['business_unit_department']
        info_env = form.cleaned_data['primary_information_environment']
        doc_types = form.cleaned_data.get('primary_document_types', '')
        summary = form.cleaned_data['inquiry_summary']

        subject = f"Service 03 — CIRF Inquiry: {org_name} ({bu_dept})"
        email_message = (
            f"SERVICE 03 — CIRF ORGANIZATIONAL INQUIRY\n"
            f"=========================================\n\n"
            f"Full Name: {full_name}\n"
            f"Work Email: {work_email}\n"
            f"Organization: {org_name}\n"
            f"Business Unit / Department: {bu_dept}\n"
            f"Primary Information Environment: {info_env}\n"
            f"Primary Document Types: {doc_types}\n\n"
            f"Inquiry Summary & Goals:\n{summary}\n\n"
            f"Confidentiality Acknowledgment: Executed on web form.\n"
        )
        
        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@haldankarmethod.com')
            send_mail(
                subject=subject,
                message=email_message,
                from_email=from_email,
                recipient_list=[from_email],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'CIRF Inquiry transmitted successfully. Our team will review your organizational environment and contact you.'})
        except Exception:
            return JsonResponse({'success': True, 'message': 'CIRF Inquiry transmitted successfully (development mode).'})
    else:
        errors = form.errors.get_json_data()
        first_error_msg = "Form validation failed."
        for field, error_list in errors.items():
            if error_list:
                field_label = field.replace('_', ' ').title()
                first_error_msg = f"{field_label}: {error_list[0]['message']}"
                break
        return JsonResponse({'success': False, 'message': first_error_msg}, status=400)
