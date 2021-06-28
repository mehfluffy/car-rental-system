from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import *


class RentForm(forms.Form):
    vehicles = Vehicle.objects.filter(available=True)
    subtype_choices = []
    for vehicle in vehicles:
        s = vehicle.subtype.subtype_name
        if (s, s) not in subtype_choices:
            subtype_choices.append((s, s))

    choose_subtype = forms.ChoiceField(
        widget=forms.Select, choices=subtype_choices
    )

    return_date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date'}, time_attrs={'type': 'time'}
        )
    )
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['return_date'] < timezone.now():
            raise ValidationError('Return date cannot be in the past')
        

class PaymentForm(forms.Form):
    fifty_euro = forms.IntegerField(
        required=True, min_value=0, initial=0, label='50 euro'
    )
    twenty_euro = forms.IntegerField(
        required=True, min_value=0, initial=0, label='20 euro'
    )
    ten_euro = forms.IntegerField(
        required=True, min_value=0, initial=0, label='10 euro'
    )
    five_euro = forms.IntegerField(
        required=True, min_value=0, initial=0, label='5 euro'
    )
    two_euro = forms.IntegerField(
        required=True, min_value=0, initial=0, label='2 euro'
    )
    one_euro = forms.IntegerField(
        required=True, min_value=0, initial=0, label='1 euro'
    )
    fifty_cent = forms.IntegerField(
        required=True, min_value=0, initial=0, label='50 cent'
    )
    twenty_cent = forms.IntegerField(
        required=True, min_value=0, initial=0, label='20 cent'
    )
    
    def __init__(self, *args, **kwargs):
        self.price = kwargs.pop('price')
        super(PaymentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        amount_paid = self.amount_paid(cleaned_data)
        amount_paid_headroom = max(Money.AMOUNT_CHOICES)[0]

        if amount_paid >= self.price + amount_paid_headroom:
            raise ValidationError('You are paying way too much!')

        elif amount_paid < self.price:
            remainder = round(self.price - amount_paid, 2)
            raise ValidationError(f'{remainder} remains to be paid.')

    def amount_paid(self, cleaned_data):
        amount_paid = 0
        for name, number in cleaned_data.items():
            amount_paid += Money.objects.get(name=name).amount * number
        return amount_paid
