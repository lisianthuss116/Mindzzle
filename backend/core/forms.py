from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICE = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '1125 Main St',
            'class':'form-control'
        }))
    apartment_address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Apartment Or Suite',
            'class':'form-control'
        }))
    country = CountryField(
        blank_label='( select country )').formfield(
            widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100 form-control'
        }))

    billing_zip = forms.CharField()
    same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_options = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICE)
