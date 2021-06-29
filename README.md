![](https://github.com/mehfluffy/car-rental-system/blob/master/asiacar/static/asiacar/logo.png)

# Description
Design of a car rental service backend according to [these requirements](https://github.com/mehfluffy/car-rental-system/blob/master/car_rental_service_intent.pdf),
implemented as a web application.

## Installation
This web app is written in Python 3 with Django. To run the app:
1. Clone the repository
1. In the repository directory, use [Pipenv](https://pipenv.pypa.io/en/latest/install/) to install the dependencies and spawn a virtual environment - ``pipenv install`` then ``pipenv shell``.
1. The database should have all the ``Vehicles`` and ``Money`` entries ready (``Money`` entries have differing numbers of bills/coins), along with two ``User``s by the ``username`` 'G-123456-SK' and 'N-12345678'. If you did not clone the database, then you'd have to set it up:
    ```
    python3 manage.py migrate
    python3 manage.py init_vehicles
    python3 manage.py init_money
    ```
    and make ``User``s via the shell:
    ```
    python3 manage.py shell
    from asiacar.models import User
    u = User(username='N-34567890', membership='R')
    u.save()
    ```
1.  Then you can run ``python3 manage.py runserver`` and go to ``127.0.0.1:8000`` to use the app. If you want to run it on a different port, just write the desired number after ``runserver``.

## Remarks
Some of the requirements specified have not been fully implemented yet. This include:
* The pincode to unlock the car is just randomly generated and displayed on the webpage right now, instead of actually being sent to the vehicle.
* The unique number for each vehicle, mentioned in the assignment, is assumed to be its primary key (=id) in the database. In real use, it might be more useful to store the license plate number instead.
* The calculation of the cashback considers the available number of each bill/coin, by taking only the ``Money`` objects that has a ``number`` greater than what the change would require.
* Delays are recorded, but the reset every month has not been implemented.
* All times are shown and recorded in UTC. In practice it would be more user-friendly to display local time.