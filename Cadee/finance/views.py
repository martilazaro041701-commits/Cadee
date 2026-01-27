from decimal import Decimal
import calendar
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import BudgetLimit, Category, PurchaseGoal, Transaction, UserProfile
from .forms import (
    BudgetLimitForm,
    LoginForm,
    ProfileForm,
    PurchaseGoalForm,
    PurchaseGoalUpdateForm,
    RegisterForm,
    TransactionForm,
)

def _build_transaction_items(transactions):
    items = []
    for txn in transactions:
        amount = txn.amount or Decimal("0.00")
        is_negative = amount < 0
        amount_display = abs(amount)
        items.append(
            {
                "description": txn.description,
                "date": txn.date,
                "folder": txn.folder,
                "amount": amount,
                "amount_display": amount_display,
                "is_negative": is_negative,
            }
        )
    return items


# Create your views here.

def dashboard(request):
    # Fetch data from folder stack, guard anonymous users.
    if request.user.is_authenticated:
        folders = Category.objects.filter(user=request.user)
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={"full_name": request.user.get_full_name() or request.user.username},
        )
        budget, _ = BudgetLimit.objects.get_or_create(user=request.user)

        transactions = (
            Transaction.objects.filter(user=request.user)
            .select_related("folder")
            .order_by("-date")
        )
        recent_transactions = transactions[:5]
        transaction_items = _build_transaction_items(recent_transactions)

        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_of_week = now - timedelta(days=7)

        zero = Value(Decimal("0.00"), output_field=DecimalField())

        total_savings = (
            transactions.aggregate(total=Coalesce(Sum("amount"), zero))["total"]
        )

        month_earnings = (
            transactions.filter(date__gte=start_of_month, amount__gt=0)
            .aggregate(total=Coalesce(Sum("amount"), zero))["total"]
        )
        month_expenses = (
            transactions.filter(date__gte=start_of_month, amount__lt=0)
            .aggregate(total=Coalesce(Sum("amount"), zero))["total"]
        )
        month_expenses_abs = abs(month_expenses)

        week_expenses = (
            transactions.filter(date__gte=start_of_week, amount__lt=0)
            .aggregate(total=Coalesce(Sum("amount"), zero))["total"]
        )
        week_expenses_abs = abs(week_expenses)

        weekly_spent = week_expenses_abs
        monthly_spent = month_expenses_abs

        weekly_limit = budget.weekly_limit or Decimal("0.00")
        monthly_limit = budget.monthly_limit or Decimal("0.00")
        weekly_percent = (
            min(Decimal("100.0"), (weekly_spent / weekly_limit) * 100)
            if weekly_limit > 0
            else Decimal("0.0")
        )
        monthly_percent = (
            min(Decimal("100.0"), (monthly_spent / monthly_limit) * 100)
            if monthly_limit > 0
            else Decimal("0.0")
        )

        weekly_left_days = max(0, 7 - now.isoweekday())
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        monthly_left_days = max(0, days_in_month - now.day)

        savings_ratio = (
            ((month_earnings - month_expenses_abs) / month_earnings) * 100
            if month_earnings > 0
            else Decimal("0.0")
        )

        goals = []
        for goal in PurchaseGoal.objects.filter(user=request.user).order_by("deadline"):
            target = goal.target_amount or Decimal("0.00")
            saved = goal.current_saved or Decimal("0.00")
            progress = (saved / target * 100) if target > 0 else Decimal("0.0")
            goals.append(
                {
                    "id": goal.id,
                    "description": goal.description,
                    "current_saved": saved,
                    "target_amount": target,
                    "deadline": goal.deadline,
                    "status": goal.status,
                    "status_label": goal.get_status_display(),
                    "image": goal.image,
                    "progress": min(Decimal("100.0"), progress),
                }
            )
    else:
        folders = Category.objects.none()
        recent_transactions = Transaction.objects.none()
        transaction_items = []
        profile = None
        budget = None
        month_earnings = Decimal("0.00")
        month_expenses_abs = Decimal("0.00")
        week_expenses_abs = Decimal("0.00")
        weekly_limit = Decimal("0.00")
        monthly_limit = Decimal("0.00")
        weekly_spent = Decimal("0.00")
        monthly_spent = Decimal("0.00")
        weekly_percent = Decimal("0.0")
        monthly_percent = Decimal("0.0")
        weekly_left_days = 0
        monthly_left_days = 0
        savings_ratio = Decimal("0.0")
        goals = []

    context = {
        'folders': folders,
        'transactions': transaction_items,
        'profile': profile,
        'total_savings': total_savings if request.user.is_authenticated else Decimal("0.00"),
        'month_earnings': month_earnings,
        'month_expenses': month_expenses_abs,
        'week_expenses': week_expenses_abs,
        'weekly_limit': weekly_limit,
        'monthly_limit': monthly_limit,
        'weekly_spent': weekly_spent,
        'monthly_spent': monthly_spent,
        'weekly_percent': weekly_percent,
        'monthly_percent': monthly_percent,
        'weekly_left_days': weekly_left_days,
        'monthly_left_days': monthly_left_days,
        'savings_ratio': savings_ratio,
        'goals': goals,
        'currency_symbol': "\u20b1",
    }

    return render(request, 'finance/dashboard.html', context)


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("dashboard")
    else:
        form = TransactionForm(user=request.user)

    return render(request, "finance/add_transaction.html", {"form": form})


@login_required
def transaction_list(request):
    transactions = (
        Transaction.objects.filter(user=request.user)
        .select_related("folder")
        .order_by("-date")
    )
    context = {
        "transactions": _build_transaction_items(transactions),
        "currency_symbol": "\u20b1",
    }
    return render(request, "finance/transactions_list.html", context)


@login_required
def edit_limits(request):
    budget, _ = BudgetLimit.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = BudgetLimitForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = BudgetLimitForm(instance=budget)

    return render(request, "finance/edit_limits.html", {"form": form})


@login_required
def add_goal(request):
    if request.method == "POST":
        form = PurchaseGoalForm(request.POST, request.FILES)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect("dashboard")
    else:
        form = PurchaseGoalForm()

    return render(request, "finance/add_goal.html", {"form": form})


@login_required
def update_goal(request, goal_id):
    goal = PurchaseGoal.objects.filter(user=request.user, id=goal_id).first()
    if goal is None:
        return redirect("dashboard")

    if request.method == "POST":
        form = PurchaseGoalUpdateForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = PurchaseGoalUpdateForm(instance=goal)

    return render(
        request,
        "finance/update_goal.html",
        {"form": form, "goal": goal},
    )


@login_required
def delete_goal(request, goal_id):
    goal = PurchaseGoal.objects.filter(user=request.user, id=goal_id).first()
    if goal is None:
        return redirect("dashboard")
    if request.method == "POST":
        goal.delete()
    return redirect("dashboard")


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"full_name": request.user.get_full_name() or request.user.username},
    )
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "finance/edit_profile.html", {"form": form})


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")


def login_screen(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "finance/login.html", {"form": form})


def register_screen(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={"full_name": user.get_full_name() or user.username},
            )
            auth_login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "finance/register.html", {"form": form})
