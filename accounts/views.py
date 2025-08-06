from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from cart.models import Cart


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')  # Redirect to home after signup
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm  # Ensure you have a LoginForm in forms.py

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)   
                cart, created = Cart.objects.get_or_create(user=user)
               
                request.session["username"] = user.username
                request.session["user_id"] = user.id
                
                messages.success(request, "Login successful!")
                return redirect("/")  # Redirect to home after login
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # ✅ Destroys the session
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")  # Redirect to login page after logout

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserUpdateForm  # Create this form

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Password updated successfully!')
            return redirect('profile')

    else:
        form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/profile.html', {'form': form, 'password_form': password_form})