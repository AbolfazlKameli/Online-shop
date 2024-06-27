from datetime import datetime, timedelta

import pytz
from celery import shared_task

from utils import send_otp_code
from .models import OtpCode


@shared_task
def send_code_task(phone_number, otp_code):
    send_otp_code(phone_number, otp_code)


@shared_task
def remove_expired_opts_task():
    expires = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expires).delete()
