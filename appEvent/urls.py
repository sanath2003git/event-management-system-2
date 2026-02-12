from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about_us/',views.about_us,name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path('events/',views.events,name='events'),
    path('event_detail/<int:id>/', views.event_detail, name='event_detail'),
    path('bookings/',views.bookings,name='bookings'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('event_create/', views.event_create, name='event_create'),
    path('my-events/', views.my_events_view, name='my_events'),
    path('manage_events/', views.manage_events, name='manage_events'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),

    path('base/', views.base, name='base'),
]