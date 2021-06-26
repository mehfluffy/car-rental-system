from django.core.management.base import BaseCommand
from asiacar.models import Money

class Command(BaseCommand):
    def _create_money(self, number_per_bill):
        money_types = Money.AMOUNT_CHOICES
        for money_type in money_types:
            entry = Money(
                amount=money_type[0], 
                name=money_type[1], 
                number=number_per_bill
            )
            entry.save()

    def handle(self, *args, **options):
        self._create_money(1000)