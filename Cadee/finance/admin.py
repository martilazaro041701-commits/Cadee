from django.contrib import admin
from .models import UserProfile, Category, Transaction, PurchaseGoal

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(PurchaseGoal)