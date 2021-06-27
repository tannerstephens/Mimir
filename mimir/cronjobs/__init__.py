from ..extensions import crontab

from .fetch_diamond_releases import fetch_diamond_releases

def register_cronjobs():
  weekly_decorator = crontab.job(minute="47", hour="16")

  weekly_decorator(fetch_diamond_releases)
