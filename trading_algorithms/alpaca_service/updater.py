from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger

from .mean_reversion_trader import MeanReversionTrader

def start():
    scheduler = BackgroundScheduler(timezone='US/Eastern')
    # scheduler programming
    # https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html
    # https://apscheduler.readthedocs.io/en/latest/userguide.html#modifying-jobs

    # This is how the half an hour form 9:30 - 10:00 can be utilised as well throughout the market hours
    # https://stackoverflow.com/a/57981158

    trader = MeanReversionTrader()

    morning = CronTrigger(day_of_week='mon-fri', hour='9', minute='30-59/1', timezone='US/Eastern')
    day = CronTrigger(day_of_week='mon-fri', hour='10-23', minute='*/1', timezone='US/Eastern')    
    trigger = OrTrigger([morning, day])
    scheduler.add_job(trader.market_check, trigger)

    scheduler.start()