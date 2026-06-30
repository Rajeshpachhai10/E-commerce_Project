from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm

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
        
