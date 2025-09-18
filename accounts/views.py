from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required


def signup(request):
    template_data = {}
    template_data["title"] = "Sign Up"

    if request.method == "GET":
        template_data["form"] = CustomUserCreationForm()
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect("accounts.login")
        else:
            template_data["form"] = form

    return render(request, "accounts/signup.html", {"template_data": template_data})


def login(request):
    template_data = {}
    template_data["title"] = "Login"

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            template_data["error"] = "The username or password is incorrect."
        else:
            auth_login(request, user)
            return redirect("home.index")

    return render(request, "accounts/login.html", {"template_data": template_data})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home.index")
