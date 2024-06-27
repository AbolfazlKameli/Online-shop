from datetime import datetime, timedelta

import pytz
from django.core.management import BaseCommand

from users.models import OtpCode


class Command(BaseCommand):
    help = 'remove all expired otp codes'

    def handle(self, *args, **options):
        expired = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
        otp_codes = OtpCode.objects.filter(created__lt=expired).exists()
        if otp_codes:
            OtpCode.objects.filter(created__lt=expired).delete()
            self.stdout.write(self.style.SUCCESS('successfully removed expired opt codes'))
        else:
            self.stdout.write('no otp codes exists')
