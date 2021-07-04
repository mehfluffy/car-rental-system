from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils import timezone

from .models import Vehicle, Rental, Subtype
from .forms import RentForm, PaymentForm
from .helpers import calculate_change, add_money, subtract_money


def home(request):
    context = {
        'user': request.user,
        'subtypes': Subtype.objects.all(),
    }
    return render(request, 'asiacar/home.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = authenticate(request, username=username)
        if user is not None:
            login(request, user)
            if user.is_renting:
                return redirect('return')
            return redirect('rent')
        else:
            return HttpResponse('Invalid credentials')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def rent_view(request):
    if request.method == 'POST':
        form = RentForm(request.POST)
        
        if form.is_valid():
            chosen_subtype = form.cleaned_data['choose_subtype']
            vehicle = Vehicle.objects.filter(
                subtype=chosen_subtype, available=True
            )[0]
            renter = request.user
            time_end = form.cleaned_data['return_date'] 

            try:
                rental = Rental.objects.create(
                    vehicle=vehicle,
                    renter=renter,
                    time_start=timezone.now(),
                    time_end=time_end
                )
            except IntegrityError:
                return HttpResponse('Invalid input')

            rental.set_pincode()
            rental.save()
            rental.vehicle.set_unavailable()
            rental.vehicle.save(update_fields=['available'])
            renter.is_renting = True
            renter.save(update_fields=['is_renting'])

            if renter.membership == 'G':
                response = redirect('rentsuccess')
            elif renter.membership == 'R':
                response = redirect('rentcheckout')
            return response
    else:
        form = RentForm()

    context = {'form': form, 'user': request.user}
    return render(request, 'asiacar/rent.html', context)


@login_required
def checkout_view(request):
    rental = Rental.objects.get(renter=request.user, time_returned=None)
    
    if request.user.membership == 'R':
        pledge = rental.vehicle.subtype.pledgeprice_reg
    else:
        pledge = 0
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, price=pledge)
        if form.is_valid():
            add_money(form)
            return redirect('rentsuccess')

    else:
        form = PaymentForm(price=pledge)

    context = {
        'user': request.user,
        'pledge': pledge,
        'form': form,        
    }
    return render(request, 'asiacar/rent_checkout.html', context)


@login_required
def checkout_success_view(request):
    rental = Rental.objects.get(renter=request.user, time_returned=None)
    context = {
        'location': rental.vehicle.park_location, 
        'pincode': rental.pincode,
    }
    return render(request, 'asiacar/rent_success.html', context)


@login_required
def return_view(request):

    rental = Rental.objects.get(renter=request.user, time_returned=None)
    rental.time_returned = timezone.now()
    rental.set_price_total()
    rental.save(update_fields=['price_total'])

    if request.method == 'POST':
        form = PaymentForm(request.POST, price=rental.price_total)
        if form.is_valid():
            add_money(form)
            amount_paid = form.amount_paid(form.cleaned_data)
            amount_change = round(amount_paid - rental.price_total, 2)

            response = redirect('returnsuccess')
            response.set_cookie('time_returned', rental.time_returned)
            response.set_cookie('amount_change', amount_change)
            return response
    
    else:
        form = PaymentForm(price=rental.price_total)

    context = {
        'user': request.user, 
        'rental': rental,
        'form': form, 
    }
    return render(request, 'asiacar/return.html', context)


@login_required
def return_success_view(request):
    renter = request.user

    rental = Rental.objects.filter(renter=request.user).last()
    rental.time_returned = request.COOKIES.get('time_returned')
    rental.save(update_fields=['time_returned'])
    rental = Rental.objects.filter(renter=request.user).last()

    rental.vehicle.available = True
    rental.vehicle.save(update_fields=['available'])
    
    renter.is_renting = False
    renter.save(update_fields=['is_renting'])

    amount_change = float(request.COOKIES.get('amount_change'))
    if (renter.membership == 'R') and (rental.get_delay()[0] == False):
        amount_change += rental.vehicle.subtype.pledgeprice_reg
    change_dict = calculate_change(amount_change)
    subtract_money(change_dict)

    context = {
        'user': renter,
        'amount_change': amount_change,
        'change': change_dict,
    }
    return render(request, 'asiacar/return_success.html', context)
