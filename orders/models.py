from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User
from home.models import Product


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ('-updated', '-paid')

    def __str__(self):
        return f'{self.user} - {self.paid}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product}'

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    expires_at = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(90, 'enter a value less than 90')])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class PayInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pay_user_info')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    reference_id = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = "PayInformation"

    def __str__(self):
        return f'{self.user} - {self.order} - {self.reference_id}'
