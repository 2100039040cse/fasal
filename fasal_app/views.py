# from django.shortcuts import render


# def index(request):
#     context={}
#     return render(request, 'fasal_app/index.html', context)

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
def index(request):
    context = {}
    return render(request, 'fasal_app/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            address = form.cleaned_data.get('address')
            # Create a Profile object for the user
            Profile.objects.create(user=user, address=address)
            login(request, user)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  # Redirect to login page after successful signup
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = SignUpForm()
    return render(request, 'fasal_app/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Error in form submission.')
    else:
        form = LoginForm()
    return render(request, 'fasal_app/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'fasal_app/home.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated! Please log in with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    # Render a form template (if you don’t want to use a separate template, handle it in the profile page instead)
    return render(request, 'fasal_app/change_password.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            request.user.delete()
            messages.success(request, 'Your account has been deleted. You can sign up again if you wish.')
            return redirect('signup')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
    
    return render(request, 'fasal_app/confirm_delete.html')

@login_required
def confirm_delete(request):
    return render(request, 'fasal_app/confirm_delete.html')

@login_required
def logout(request):
    return render(request, 'fasal_app/index.html')

# @login_required
# def profile(request):
#     return render(request, 'fasal_app/profile.html')
@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user, defaults={'address': 'No address provided'})
    return render(request, 'fasal_app/profile.html', {'profile': user_profile})
@login_required
def long_listening(request):
    return render(request, 'fasal_app/long_listening.html')

@login_required
def text_to_speech(request):
    return render(request, 'fasal_app/text_to_speech.html')
