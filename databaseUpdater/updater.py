from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler

from databaseUpdater import userApi


def start():
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(userApi.reset_delays, 'cron', day=1, hour=0)
    scheduler.start()
