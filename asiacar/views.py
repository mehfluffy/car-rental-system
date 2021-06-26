from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.utils import timezone

from .models import *
from .forms import *
from .helpers import calculate_change


def home(request):
    context = {'user': request.user}
    return render(request, 'asiacar/home.html', context)
# a ListView of the prices?


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
    
    context = {
        'user': request.user,
        'pledge': pledge,
        'location': rental.vehicle.park_location, 
        'pincode': rental.pincode,
    }
    return render(request, 'asiacar/rent_checkout.html', context)


@login_required
def return_view(request):

    rental = Rental.objects.get(renter=request.user, time_returned=None)
    rental.time_returned = timezone.now()
    rental.set_price_total()
    rental.save(update_fields=['price_total'])

    if request.method == 'POST':
        form = ReturnForm(request.POST, price_total=rental.price_total)
        if form.is_valid():
            amount_paid = 0
            for field in form:
                money = Money.objects.get(name=field.name)
                number = int(field.value())
                money.number += number
                money.save()
                amount_paid += money.amount * number
            
            amount_change = round(amount_paid - rental.price_total, 2)
            response = redirect('returnsuccess')
            response.set_cookie('time_returned', rental.time_returned)
            response.set_cookie('amount_change', amount_change)
            return response
    
    else:
        form = ReturnForm(price_total=rental.price_total)

    context = {
        'form': form, 
        'user': request.user, 
        'rental': rental,
    }
    return render(request, 'asiacar/return.html', context)


@login_required
def success_view(request):
    renter = request.user
    amount_change = request.COOKIES.get('amount_change')
    change = calculate_change(amount_change)
    
    rental = Rental.objects.get(renter=request.user, time_returned=None)
    rental.time_returned = request.COOKIES.get('time_returned')
    rental.vehicle.available = True
    rental.save(update_fields=['time_returned'])
    rental.vehicle.save(update_fields=['available'])
    
    renter.is_renting = False
    renter.save(update_fields=['is_renting'])

    context = {
        'user': renter,
        'amount_change': amount_change,
        'change': change,
    }
    return render(request, 'asiacar/return_success.html', context)


"""
class SignUp(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('signupsuccess')

def signup_success(request):

    # put this in helpers.py
    def create_user(form):
        membership = form.cleaned_data['membership']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        
        
        initials = []
        if membership == 'G':
            letter = 'G'
            k = 6
            for name in [first_name, last_name]:
                initials.append(name[0].upper())
        elif membership == 'R':
            letter = 'N'
            k = 8
        num = ''.join(random.choices(string.digits, k=6))
        username = '-'.join([letter, num, initials])
        user = User.objects.create(
            membership=membership, username=username,
            first_name=first_name, last_name=last_name,
        )
        try:
            user.save()
        except IntegrityError:
            create_user(form)
        return user

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = create_user(form)
            context = {'username': user.username}
            return render(request, 'registration/signup_success.html', context)
    else:
        form = UserForm()
        context = {}
    return redirect()
"""