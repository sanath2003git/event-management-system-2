from django.shortcuts import render, redirect
from .forms import UserSignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import User
from .forms import LoginForm 
from django.contrib.auth import logout
from appEvent.models import Event,Booking  
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # make sure 'login' exists in urls.py
        else:
            print(form.errors)  # Debug form errors in terminal
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)

                # Role-based redirection
                if user.role == User.Role.ORGANIZER:
                    return redirect('organizer_dashboard')
                elif user.role == User.Role.ATTENDEE:
                    return redirect('attendee_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')


#organizer_dashboard

@login_required
def organizer_dashboard_view(request):
    latest_events=Event.objects.order_by('-id')[:4]
    context={
        'latest_events':latest_events
    }
    return render (request,'organizer_dashboard.html',context)

#attendee_dashboard
@login_required
def attendee_dashboard_view(request):
    latest_events=Event.objects.order_by('-id')[:4]
    context={
        'latest_events':latest_events
    }
    return render(request, 'attendee_dashboard.html',context)

@login_required
def user_profile(request):
    user = request.user
    bookings = None
    events = None

    if user.role == "ATTENDEE":
        bookings = Booking.objects.filter(user=user)
    elif user.role == "ORGANIZER":
        events = Event.objects.filter(created_by=user)  # Assuming you track creator

    return render(request, "profile.html", {
        "bookings": bookings,
        "events": events,
    })