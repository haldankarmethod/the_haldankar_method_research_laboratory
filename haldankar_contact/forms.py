from django import forms

class CollaborationInquiryForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    inquiry_area = forms.CharField(max_length=255, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_honeypot(self):
        val = self.cleaned_data.get('honeypot')
        if val:
            raise forms.ValidationError("Spam detected.")
        return val


class CIRFInquiryForm(forms.Form):
    ENVIRONMENT_CHOICES = [
        ('', 'Select Primary Information Environment...'),
        ('financial', 'Financial Disclosures / Equity & Credit Research'),
        ('legal', 'Legal Contracts & Regulatory Compliance'),
        ('risk', 'Risk & Quantitative Decision Context Models'),
        ('technical', 'Healthcare & Technical Documentation'),
        ('corporate', 'Corporate Operations & Internal Workflows'),
    ]

    full_name = forms.CharField(max_length=255, required=True)
    work_email = forms.EmailField(required=True)
    organization_name = forms.CharField(max_length=255, required=True)
    business_unit_department = forms.CharField(max_length=255, required=True)
    primary_information_environment = forms.ChoiceField(choices=ENVIRONMENT_CHOICES, required=True)
    primary_document_types = forms.CharField(max_length=255, required=False)
    inquiry_summary = forms.CharField(widget=forms.Textarea, required=True)
    confidentiality_acknowledgment = forms.BooleanField(required=True)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_honeypot(self):
        val = self.cleaned_data.get('honeypot')
        if val:
            raise forms.ValidationError("Spam detected.")
        return val
