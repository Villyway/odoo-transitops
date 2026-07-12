from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import SignUpForm


class TransitLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True


class TransitLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard:home")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})
