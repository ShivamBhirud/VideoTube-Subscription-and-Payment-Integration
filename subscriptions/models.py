from django.db import models
from django.contrib.auth.models import User


class Subscriptions(models.Model):
    plan = models.IntegerField(default=0, null=True)
    is_active = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)
    remaining_days = models.IntegerField(null=True, blank=True)
    logged_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.plan
    


