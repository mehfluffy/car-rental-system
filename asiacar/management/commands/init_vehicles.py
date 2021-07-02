from string import ascii_uppercase

from django.core.management.base import BaseCommand

from asiacar.models import Subtype, Vehicle


class Command(BaseCommand):

    def _create_subtypes(self):
        subtype_name = Subtype.subtype_name_choices
        hourprice_gold = [
            3.75, 3.85, 3.95, 3.95, 3.95, 3.95, 3.95,
            8.75, 8.85, 8.95, 
            2.95, 2.95, 2.95, 
            17.5, 17.5, 17.5, 17.5, 
            25.0, 25.0, 
            25.0, 55.0, 19.5, 35.0,
        ]
        hourprice_reg = [
            5.05, 5.15, 5.25, 5.35, 5.35, 5.35, 5.35, 
            9.45, 9.55, 9.65, 
            3.15, 3.15, 3.15, 
            19.0, 19.0, 19.0, 19.0, 
            30.0, 30.05, 
            30.0, 64.0, 23.5, 40.0,
        ]
        pledgeprice_reg = []
        for subtype in subtype_name:  # 23 subtypes
            if subtype[0] == 'L' or 'M' or 'N':
                pledge = 100.0
            else:
                pledge = 300.0
            pledgeprice_reg.append(100.0)
        
        entries = []
        for i in range(len(subtype_name)):
            entry = Subtype(
                subtype_name=subtype_name[i], 
                hourprice_gold = hourprice_gold[i],
                hourprice_reg = hourprice_reg[i],
                pledgeprice_reg = pledgeprice_reg[i]
            )
            entries.append(entry)
            entry.save()
        return entries


    def _create_vehicles(self, vehicles_per_subtype):
        letters = list(ascii_uppercase)
        subtypes = self._create_subtypes()

        for i in range(len(subtypes)):
            for j in range(vehicles_per_subtype):
                entry = Vehicle(
                    subtype=subtypes[i], 
                    park_location=letters[i]+str(j)
                )
                entry.save()


    def handle(self, *args, **options):
        self._create_vehicles(2)  # can extend vehicles_per_subtype to an arg
