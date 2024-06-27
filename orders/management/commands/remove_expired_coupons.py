from datetime import datetime

import pytz
from django.core.management import BaseCommand

from orders.models import Coupon


class Command(BaseCommand):
    help = 'remove Unbound coupons'

    def handle(self, *args, **options):
        now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
        coupons = Coupon.objects.filter(expires_at__lt=now).exists()
        if coupons:
            Coupon.objects.filter(expires_at__lt=now).delete()
            self.stdout.write(self.style.SUCCESS('removed unbound coupons'))
        else:
            self.stdout.write('there is no unbound coupon')
