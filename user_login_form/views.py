from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="login")
def home(request):
    return render(request, "user_login_form/main.html")


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
    # if request from form is post then do this
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():  # Django makes validation easy
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(
                    request, 'Account was created for ' + user + ', thanks!')
                return redirect('login')
    context = {'form': form}
    return render(request, "user_login_form/register.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        # if request from form is post then do this
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Please check Username or Password")
        context = {}
        return render(request, "user_login_form/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')
