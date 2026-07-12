from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Expense
from .forms import ExpenseForm


@login_required
def expense_list(request):
    expenses = Expense.objects.select_related("vehicle").order_by("-date")
    return render(request, "expenses/expense_list.html", {"expenses": expenses})


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense recorded.")
            return redirect("expenses:list")
    else:
        form = ExpenseForm()
    return render(request, "expenses/expense_form.html", {"form": form, "title": "Record Expense"})
