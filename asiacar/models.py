from django.contrib.auth.models import AbstractUser
from django.db import models

from math import ceil
import random
import string


class Subtype(models.Model):
    subtype_name_choices = [
        'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7',
        'M1', 'M2', 'M3',
        'N1', 'N2', 'N3',
        'O1', 'O2', 'O3', 'O4',
        'T', 'G',
        'SA', 'SB', 'SC', 'SD',
    ]
    SUBTYPE_NAME_CHOICES = [(i, i) for i in subtype_name_choices]

    subtype_name = models.CharField(
        primary_key=True, max_length=2, choices=SUBTYPE_NAME_CHOICES
    )
    hourprice_gold = models.FloatField()
    hourprice_reg = models.FloatField()
    pledgeprice_reg = models.FloatField()

    def __str__(self):
        return self.subtype_name


class Vehicle(models.Model):
    # unique number = auto primary key
    subtype = models.ForeignKey(Subtype, on_delete=models.CASCADE)
    park_location = models.CharField(max_length=5)
    available = models.BooleanField(db_column='available', default=True)

    def set_unavailable(self):
        self.available = False

    def __str__(self):
        return str(self.id) + ", " + self.subtype.subtype_name + ", " + str(self.available)
"""
    @property
    def available(self):
        return self._available

    @available.setter 
    def available(self, value):
        self._available = value
"""

class User(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('G', 'Gold'),
        ('R', 'Regular')
    ]
    membership = models.CharField(choices=MEMBERSHIP_CHOICES, max_length=1, default='R')
    username = models.CharField(max_length=11, unique=True, null=True)  # membership number
    delays_thismonth = models.IntegerField(default=0)
    is_renting = models.BooleanField(default=False)
    password = models.CharField(max_length=1, default=0)
    
    def reset_delays_thismonth(self):  # reset delays monthly
        self.delays_thismonth = 0


class Rental(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    renter = models.ForeignKey(User, on_delete=models.PROTECT)
    pincode = models.IntegerField(null=True)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    time_returned = models.DateTimeField(null=True)
    price_total = models.FloatField(null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(time_end__gt=models.F('time_start')),
                name='time_end constraint'
            )
        ]

    def set_pincode(self):
        if not self.pincode:
            self.pincode = ''.join(random.choices(string.digits, k=6))

    def set_price_total(self):
        if not self.price_total:

            subtype = self.vehicle.subtype
            renter = self.renter

            seconds = (self.time_end - self.time_start).total_seconds()
            num_hours = ceil(seconds / (60*60))
            if num_hours < 4:
                num_hours = 4

            delayed = self.time_returned > self.time_end
            delay = (self.time_returned - self.time_end).total_seconds()

            price = 0.0
            if renter.membership == 'G':
                if delayed:
                    num_delays = delay / (60*30)
                    renter.delays_thismonth += num_delays
                    
                    if renter.delays_thismonth > 4:
                        num_hours += ceil(delay / (60*60))
                
                price += subtype.hourprice_gold * num_hours

            elif renter.membership == 'R':
                if delayed:
                    num_hours += ceil(delay / (60*60))
                    price += subtype.pledgeprice_reg  # not refunded if delayed
                price += subtype.hourprice_reg * num_hours

            self.price_total = round(price, 2)


class Money(models.Model):
    AMOUNT_CHOICES = [
        (50.0, 'fifty_euro'),
        (20.0, 'twenty_euro'),
        (10.0, 'ten_euro'),
        (5.0, 'five_euro'),
        (2.0, 'two_euro'),
        (1.0, 'one_euro'),
        (0.5, 'fifty_cent'),
        (0.2, 'twenty_cent'),
    ]
    amount = models.FloatField(choices=AMOUNT_CHOICES)  # currency amount, e.g. 0.50
    name = models.CharField(max_length=30, unique=True)  # name of the bill/coin e.g. 50 cents
    number = models.IntegerField()  # number of this bill/coin in the automat

"""
    def set_vehicle_unavailable(self):
        vehicle = Vehicle.objects.get(id=self.vehicle.id)
        vehicle.available = False

    def set_vehicle_available(self):
        vehicle = Vehicle.objects.get(id=self.vehicle.id)
        vehicle.available = True
"""

"""
    def set_time_start(self):
        if not self.time_start:
            self.time_start = datetime.now()

    def set_time_returned(self):
        if not self.time_returned:
            self.time_returned = datetime.now()
"""
