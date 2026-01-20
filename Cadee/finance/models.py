from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

#1 Main Dashboard Metadata
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    total_savings = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.full_name

#2 The "Folder" Logic
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    color_hex = models.CharField(max_length=7, default="#C6F4D6")
    icon_name = models.CharField(max_length=20, blank=True) 

    def __str__(self):
        return f"{self.name} Folder"

#3 Transaction History
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

#4 Purchase Goals (Analytics & Wants)
class PurchaseGoal(models.Model):
    class Status(models.TextChoices):
           PRIORITY = 'PR', 'Priority'
           WANT = 'WT', 'Want'
           IMPULSE = 'IM', 'Impulse'
           ACHIEVED = 'AC', 'Achieved'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_saved = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='goals/', blank=True, null=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.WANT)
    deadline = models.DateField()

#5 Limits
class BudgetLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    weekly_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
