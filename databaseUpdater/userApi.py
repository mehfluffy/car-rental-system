from asiacar.models import User


def reset_delays():
    users = User.objects.all()
    
    for user in users:
        user.reset_delays_thismonth()
        user.save()
