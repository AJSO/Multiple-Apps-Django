from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class LeaveApplicationModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('waiting', 'WAITING'),
        ('approved', 'APPROVED'),
        ('declined', 'DECLINED'),
    )
    leave_type = models.CharField(max_length=150)
    leave_start_date  = models.DateField()
    leave_end_date = models.DateField()
    leave_start_time = models.TimeField()
    leave_end_time = models.TimeField()
    leave_reason = models.TextField()
    status = models.CharField(max_length = 30, choices = STATUS_CHOICES, default = "waiting")
    days = models.IntegerField(default=0)

class UserDetails(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    annual_leave_days = models.IntegerField(blank=True)
    annual_leave_limit = models.IntegerField(blank=True)

