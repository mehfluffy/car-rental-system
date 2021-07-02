from decimal import Decimal

from .models import Money


def add_money(payment_form):
    for field in payment_form:
        money = Money.objects.get(name=field.name)
        number = int(field.value())
        money.number += number
        money.save(update_fields=['number'])


def subtract_money(change_dict):
    for name, number in change_dict.items():
        money = Money.objects.get(name=name)
        money.number -= number
        money.save(update_fields=['number'])


def calculate_change(change_amount):
    change_amount = Decimal(change_amount)
    if change_amount != change_amount.quantize(Decimal('.01')):  # check cents
        change_amount = cents_rounding(change_amount)

    money_available = list(Money.objects.exclude(number=0))
    if change_amount / Decimal('0.2') % 1 == 0:  # amounts like xx.60, xx.80
        money_available.remove(Money.objects.get(amount=0.5))  # don't do 50 cents

    change_dict = {}
    while money_available:
        current_coin = money_available.pop(0)
        current_amount = Decimal(str(current_coin.amount))
        number = change_amount // current_amount
        
        if number <= current_coin.number:  # if have enough bills to make the change
            change_amount = change_amount % current_amount
            if number > 0:
                change_dict[current_coin.name] = number
    
    return change_dict


def cents_rounding(change_amount):
    if change_amount % 1 <= 0.4:
        modifier = Decimal('0.2')
    else:
        modifier = Decimal('0.1')
    return change_amount + modifier - (change_amount % modifier)
    