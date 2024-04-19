from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages

class Item(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='item_pictures/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=14)
    acquired = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Auto DateTime field
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_items')
    def save(self, *args, **kwargs):
        if self.deposit > self.price:
            messages.error(None, "Deposit cannot exceed the price.")
        elif self.deposit == self.price:
            self.acquired = True
        super(Item, self).save(*args, **kwargs)
