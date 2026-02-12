from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .form import EventForm, ContactForm
from .models import Event, Booking


def home(request):
    latest_events = Event.objects.order_by('-id')[:4]
    categories = ["Music", "Art", "Sports", "Workshops", "Food", "Family"]
    return render(request, 'home page.html', {
        'latest_events': latest_events,
        'categories': categories,
    })


def events(request):
    category = request.GET.get("category")  # e.g. ?category=Music
    events = Event.objects.all().order_by('-id')

    if category:
        events = events.filter(category=category)

    # Pagination
    paginator = Paginator(events, 6)  # 6 events per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "events.html", {
        "latest_events": page_obj,
        "page_obj": page_obj,
        "selected_category": category,
        "categories": [c[0] for c in Event.CATEGORY_CHOICES],  # pass list of categories
    })


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    already_booked = False
    if request.user.is_authenticated:
        already_booked = Booking.objects.filter(user=request.user, event=event).exists()

    return render(request, 'event_details.html', {
        'event': event,
        'already_booked': already_booked,
    })


@login_required
def bookings(request):
    user_bookings = Booking.objects.filter(user=request.user).select_related('event').order_by('-booked_at')
    return render(request, 'booking.html', {'bookings': user_bookings})


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if Booking.objects.filter(user=request.user, event=event).exists():
        messages.info(request, "You have already booked this event.")
    else:
        Booking.objects.create(user=request.user, event=event)
        messages.success(request, f"You have successfully booked {event.title}.")
    return redirect('event_detail', id=event.id)

def about_us(request):
    stats = [
        {"stat": "50,000+", "desc": "Events Created"},
        {"stat": "2M+", "desc": "Tickets Sold"},
        {"stat": "15,000+", "desc": "Active Organizers"},
        {"stat": "25+", "desc": "Countries Served"},
    ]

    values = [
        {"icon": "fas fa-users", "title": "Community First", "desc": "We prioritize building strong relationships with our users and partners"},
        {"icon": "fas fa-lightbulb", "title": "Innovation", "desc": "We constantly evolve to meet the changing needs of event organizers"},
        {"icon": "fas fa-shield-alt", "title": "Trust & Security", "desc": "We ensure the highest standards of data protection and reliability"},
    ]

    return render(request, "about us.html", {"stats": stats, "values": values})


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # automatically assigns the logged-in user
            event.save()
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@login_required
def manage_events(request):
    events = Event.objects.all().order_by('-id')
    if not events:
        messages.warning(request, "No events available.")
    return render(request, 'manage_events.html', {'events': events})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST,  request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("manage_events")
    else:
        form = EventForm(instance=event)
    return render(request, "edit_event.html", {"form": form, "event": event})



@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.delete()
        return redirect("manage_events")
    return render(request, "delete_event.html", {"event": event})

@login_required
def my_events_view(request):
    user = request.user
    context = {}

    if user.role == "ATTENDEE":
        bookings = Booking.objects.filter(user=user).select_related('event').order_by('-booked_at')
        context['bookings'] = bookings

    elif user.role == "ORGANIZER":
        events_list = Event.objects.filter(created_by=user).order_by('-date')
        paginator = Paginator(events_list, 8)  # 8 events per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['events'] = page_obj.object_list
        context['page_obj'] = page_obj

    return render(request, 'my_events.html', context)


@login_required
def manage_bookings(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")
        booking = get_object_or_404(Booking, id=booking_id)

        if action == "confirm":
            booking.status = "Confirmed"
            booking.save()
            messages.success(request, f"Booking for {booking.event.title} has been confirmed.")
        elif action == "cancel":
            booking.status = "Cancelled"
            booking.save()
            messages.warning(request, f"Booking for {booking.event.title} has been cancelled.")

        return redirect("manage_bookings")

    bookings = Booking.objects.select_related("user", "event").order_by("-booked_at")
    return render(request, "manage_booking.html", {"bookings": bookings})



def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.success(request, f"If an account with {email} exists, a reset link has been sent.")
    return render(request, 'password_reset.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect('contact_us')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def base(request):
    latest_events = Event.objects.order_by('-id')[:4]
    categories = ["Music", "Art", "Sports", "Workshops", "Food", "Family"]
    return render(request, 'base.html', {
        'latest_events': latest_events,
        'categories': categories,
    })