from datetime import datetime, timedelta

import pytz
from celery import shared_task

from .models import Order, Coupon


@shared_task
def remove_expired_orders_task():
    expired = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(days=1)
    Order.objects.filter(created__lt=expired, paid=False).delete()


@shared_task
def remove_expired_coupons_task():
    now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
    Coupon.objects.filter(expires_at__lt=now).delete()
