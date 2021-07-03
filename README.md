![](https://github.com/mehfluffy/car-rental-system/blob/master/asiacar/static/asiacar/logo.png)

# Description
Design of a car rental service backend according to [these requirements](https://github.com/mehfluffy/car-rental-system/blob/master/car_rental_service_intent.pdf),
implemented as a web application.

## Installation
This web app is written in Python 3 with Django. To run the app:
1. Clone the repository
1. In the repository directory, use [Pipenv](https://pipenv.pypa.io/en/latest/install/) to install the dependencies and spawn a virtual environment - ``pipenv install`` then ``pipenv shell``.
1. The database should have all the ``Vehicles`` and ``Money`` entries ready (``Money`` entries have differing ``number``s of bills/coins), along with two ``User``s by the ``username`` 'G-123456-SK' and 'N-12345678'. If you did not clone the database, then you'd have to set it up:
    ```
    $ python3 manage.py migrate
    $ python3 manage.py init_vehicles
    $ python3 manage.py init_money
    ```
    and make ``User``s via the shell:
    ```
    $ python3 manage.py shell
    >>> from asiacar.models import User
    >>> u = User(username='N-34567890', membership='R')
    >>> u.save()
    ```
1.  Then you can run ``python3 manage.py runserver --noreload`` and go to ``127.0.0.1:8000`` with your favourite browser to try out the app. If you want to run the app on a different port, just write the desired number after ``runserver``. The option ``--noreload`` is needed so that periodic tasks will not be duplicated.

## Remarks
* The calculation of the cashback considers the available number of each bill/coin, by using only the ``Money`` objects that has a ``number`` greater than what the change would require. There is however no solution for when the change cannot be made at all with the available ``Money`` objects. Consider an example: a change of 40 cents is required, but there are no more 20 cents available. A human would probably try to give out 50 cents and ask the customer for 10 cents back. However, this programme does not even consider giving 50 cents for amounts that are multiple of 20 cents, due to change optimization. A workaround for this would be to periodically check the database to alert the admin whenever a certain bill/coin is low in numbers, so that the automat can be refilled.
* All times are recorded in UTC, but shown in the locale's timezone. The locale Amsterdam is hardcoded into [``asiacar/middleware.py``](https://github.com/mehfluffy/car-rental-system/blob/master/asiacar/middleware.py). If the rental company sets up a branch in a different timezone, but want to use the same backend, then it would be necessary to enable changing locales (perhaps through a form by the user).
* Delays are recorded, and reset every first of the month at 00:00 UTC. UTC is used to avoid the scheduled job not running or running twice in case of daylight saving time (DST). The locale (Amsterdam) uses daylight saving, which means the delays are reset at either 01:00 or 02:00 local time. In practice it would be a good idea to set the reset time such that the local version is within the closed hours of the rental business, when vehicle returns are not possible, so that customers will not have to think about DST differences when they are already delayed.


Some of the requirements specified have not been optimally implemented yet. This include:
* The pincode to unlock the car is just randomly generated and displayed on the webpage right now, instead of actually being sent to the vehicle.
* The unique number for each vehicle, mentioned in the assignment, is assumed to be its primary key (=id) in the database. In real use, it might be more useful to store the license plate number instead.
