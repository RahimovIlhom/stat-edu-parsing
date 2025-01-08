from celery import shared_task
from asgiref.sync import async_to_sync
from .scraper import scrape_and_save_statistics

@shared_task
def update_statistics():
    """Celery task to update statistics daily"""
    async_to_sync(scrape_and_save_statistics)()
