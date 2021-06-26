from .models import Money


def calculate_change(change_amount):
    change_amount = float(change_amount)
    change_amount = silly_rounding(change_amount)

    money_available = list(Money.objects.exclude(number=0))
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