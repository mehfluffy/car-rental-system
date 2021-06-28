from .models import Money


def add_money(payment_form):
    for field in payment_form:
        money = Money.objects.get(name=field.name)
        number = int(field.value())
        money.number += number
        money.save(update_fields=['number'])


def subtract_money(change_dict):
    for name, number in change_dict.items():
        money = Money.objects.get(name=field.name)
        money.number -= number
        money.save(update_fields=['number'])


def calculate_change(change_amount):
    change_amount = float(change_amount)
    change_amount = silly_rounding(change_amount)

    money_available = list(Money.objects.exclude(number=0))
    if change_amount / 0.2 == int(change_amount / 0.2):  # amounts like xx.60, xx.80
        money_available.remove(Money.objects.get(amount=0.5))  # don't do 50 cents

    change_dict = {}
    while money_available:
        current_coin = money_available.pop(0)
        number = int(change_amount / current_coin.amount)
        if number > 0:
            change_dict[current_coin.name] = number
        change_amount = round(change_amount % current_coin.amount, 2)
    return change_dict


def silly_rounding(change_amount):
    if change_amount % 1 <= 0.4:
        result = change_amount + 0.2 - (change_amount % 0.2)
    else:
        result = change_amount + 0.1 - (change_amount % 0.1)
    return round(result, 2)