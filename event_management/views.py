from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from events.models import EventCategory, Event
from .forms import LoginForm, CustomUserCreationForm

def dashboard(request):
    # If user is not authenticated, redirect to public events
    if not request.user.is_authenticated:
        return redirect('public-events')
    
    # If user is not staff/admin, redirect to user dashboard
    if not request.user.is_staff:
        return redirect('user-dashboard')
    
    # Admin dashboard data
    user = User.objects.count()
    event_ctg = EventCategory.objects.count()
    event = Event.objects.count()
    complete_event = Event.objects.filter(status='completed').count()
    events = Event.objects.all()
    context = {
        'user': user,
        'event_ctg': event_ctg,
        'event': event,
        'complete_event': complete_event,
        'events': events,
        'is_admin': True
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def user_dashboard(request):
    """Dashboard for regular users (non-admin)"""
    from events.models import EventMember
    
    # Get user's registered events - ONLY for current user
    user_events = EventMember.objects.filter(user=request.user, status='active')
    available_events = Event.objects.filter(status='active')[:5]  # Show 5 latest events
    
    context = {
        'user_events': user_events,
        'available_events': available_events,
        'user': request.user,
        'is_admin': False
    }
    return render(request, 'user_dashboard.html', context)

def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        print("POST request received for login")
        forms = LoginForm(request.POST)
        print(f"Form data: {request.POST}")
        if forms.is_valid():
            print("Form is valid")
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            print(f"Attempting to authenticate user: {username}")
            user = authenticate(username=username, password=password)
            print(f"Authentication result: {user}")
            if user:
                print("User authenticated successfully, logging in...")
                login(request, user)
                print("User logged in, redirecting to dashboard")
                return redirect('dashboard')
            else:
                print("Authentication failed - invalid credentials")
                messages.error(request, 'Invalid username or password.')
        else:
            print(f"Form is invalid. Errors: {forms.errors}")
    context = {
        'form': forms
    }
    return render(request, 'login.html', context)

def logut_page(request):
    logout(request)
    return redirect('login')

def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {username}! Please check your email at {email} for verification. You can now log in.')
            return redirect('login')
        else:
            # Add form errors to messages for better user feedback
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form
    }
    return render(request, 'register.html', context)