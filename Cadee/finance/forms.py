from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import BudgetLimit, PurchaseGoal, Transaction, UserProfile


# Creating Transactions
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["folder", "description", "amount", "date"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["folder"].queryset = self.fields["folder"].queryset.filter(user=user)

#Weekly and Monthly Budget limit setter
class BudgetLimitForm(forms.ModelForm):
    class Meta:
        model = BudgetLimit
        fields = ["weekly_limit", "monthly_limit"]

#Creating "Save Goals"
class PurchaseGoalForm(forms.ModelForm):
    class Meta:
        model = PurchaseGoal
        fields = ["description", "target_amount", "current_saved", "image", "status", "deadline"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }

#Updating Save Goal Forms
class PurchaseGoalUpdateForm(forms.ModelForm):
    class Meta:
        model = PurchaseGoal
        fields = ["current_saved", "status"]

#User Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["full_name", "profile_image"]

#Login From 
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "auth-input", "placeholder": "Username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "auth-input", "placeholder": "Password"}
        )

#Register New User
class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Choose a username",
            "password1": "Create a password",
            "password2": "Confirm password",
        }
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "auth-input", "placeholder": placeholders.get(name, "")}
            )
            field.help_text = ""
