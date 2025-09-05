from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Base user model
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        ORGANIZER = "ORGANIZER", 'Organizer'
        ATTENDEE = "ATTENDEE", 'Attendee'

    # Role field with default
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)
    # ✅ New profile picture field
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True,default="profile_pics/profile_pic_default.jpg")

    def save(self, *args, **kwargs):
        # Only assign base_role if role is not already set
        if not self.pk and not self.role:
            self.role = self.base_role
        super().save(*args, **kwargs)

        
class OrganizerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ORGANIZER)

class Organizer(User):
    base_role = User.Role.ORGANIZER
    objects = OrganizerManager()  # ✅ Use `objects`, not `organizer`

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Organizer"

    
class AttendeeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ATTENDEE)

class Attendee(User):
    base_role = User.Role.ATTENDEE
    objects = AttendeeManager()  # ✅ Use `objects`, not `attendee`

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Attendee"
