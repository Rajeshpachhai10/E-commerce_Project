from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm , ProfileForm
from .models import *
from payments.models import Order

# Create your views here.

def register(request):
    form=RegisterForm()
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request ,"Account created successfully")
            return redirect('login')
        else:
            messages.error(request,"Please fix the errors below!")
    return render(request , 'accounts/register.html' , {'form':form})



def log_in(request):
    form = LoginForm(request)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            remember_me = request.POST.get('remember_me')
            if remember_me:
                request.session.set_expiry(1209600)  # 14 days
            else:
                request.session.set_expiry(0)  # browser close

            next_url = request.POST.get('next', '')
            return redirect(next_url if next_url else 'index')
        else:
            messages.error(request, "Invalid email or password.")

    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def log_out(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')



@login_required(login_url='login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, "Password changed successfully!")
            return redirect('index')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/password_change.html', {'form': form})



'''
=======================Profile Management========================================================
'''
@login_required(login_url="login")
def profile_dashboard(request):
    return render(request,"profile/dashboard.html")


@login_required(login_url="login")
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, "profile/profile.html", context)


@login_required(login_url="login")
def my_order(request):
    orders = (
        Order.objects
        .filter(transaction__user=request.user)
        .select_related('transaction')
        .prefetch_related('items')
        .order_by('-transaction__created_at')
    )
    return render(request, "profile/my_order.html", {"orders": orders})
        
