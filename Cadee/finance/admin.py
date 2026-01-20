from django.contrib import admin
from .models import BudgetLimit, Category, PurchaseGoal, Transaction, UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "total_savings")
    search_fields = ("full_name", "user__username")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color_hex")
    search_fields = ("name", "user__username")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "amount", "folder", "user")
    list_filter = ("folder", "date")
    search_fields = ("description", "user__username")
    ordering = ("-date",)


@admin.register(PurchaseGoal)
class PurchaseGoalAdmin(admin.ModelAdmin):
    list_display = ("description", "user", "target_amount", "current_saved", "deadline", "status")
    list_filter = ("status", "deadline")
    search_fields = ("description", "user__username")


@admin.register(BudgetLimit)
class BudgetLimitAdmin(admin.ModelAdmin):
    list_display = ("user", "weekly_limit", "monthly_limit")
