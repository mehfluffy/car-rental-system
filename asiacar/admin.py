from django.contrib import admin

from .models import Subtype, Vehicle, User, Rental


for model in [Subtype, Vehicle, User, Rental]:
    admin.site.register(model)