from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):

    CATEGORY_CHOICES = [
        ("Music", "Music"),
        ("Art", "Art"),
        ("Sports", "Sports"),
        ("Workshops", "Workshops"),
        ("Food", "Food"),
        ("Family", "Family"),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField()

    date = models.DateField(default=timezone.now)

    start_at = models.TimeField(default='08:00:00')

    end_at = models.TimeField(default='08:00:00')

    location = models.CharField(max_length=255)

    image = models.ImageField(
        upload_to='event_images/',
        default='event_images/default_event_image.jpg'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Music"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

    class Meta:
        db_table = "event"


class Booking(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"