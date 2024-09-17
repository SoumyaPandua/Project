from django.db import models
from django.utils import timezone
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True)
    razorpay_order_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_items = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('pending', 'Pending'), ('failed', 'Failed')])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.order_id} for {self.user.username}"

