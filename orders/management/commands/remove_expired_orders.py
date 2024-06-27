from datetime import timedelta, datetime

import pytz
from django.core.management import BaseCommand

from orders.models import Order


class Command(BaseCommand):
    help = 'remove expired orders'

    def handle(self, *args, **options):
        expired = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(days=1)
        orders = Order.objects.filter(updated__lt=expired, paid=False).exists()
        if orders:
            Order.objects.filter(updated__lt=expired).delete()
            self.stdout.write(self.style.SUCCESS('removed expired orders'))
        else:
            self.stdout.write('no expired orders exists')
