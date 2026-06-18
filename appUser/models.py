from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):

        ADMIN = "ADMIN", "Admin"

        ORGANIZER = "ORGANIZER", "Organizer"

        ATTENDEE = "ATTENDEE", "Attendee"


    role = models.CharField(

        max_length=50,

        choices=Role.choices,

        default=Role.ATTENDEE
    )


    profile_pic = models.ImageField(

        upload_to="profile_pics/",

        blank=True,

        null=True,

        default="profile_pics/profile_pic_default.jpg"
    )


    def save(self, *args, **kwargs):

        if hasattr(self, "base_role"):

            if not self.role:

                self.role = self.base_role

        super().save(*args, **kwargs)



class OrganizerManager(UserManager):

    def get_queryset(self):

        return super().get_queryset().filter(

            role=User.Role.ORGANIZER

        )



class Organizer(User):

    base_role = User.Role.ORGANIZER

    objects = OrganizerManager()


    class Meta:

        proxy = True

        verbose_name = "Organizer"

        verbose_name_plural = "Organizers"


    def welcome(self):

        return "Only for Organizer"



class AttendeeManager(UserManager):

    def get_queryset(self):

        return super().get_queryset().filter(

            role=User.Role.ATTENDEE

        )



class Attendee(User):

    base_role = User.Role.ATTENDEE

    objects = AttendeeManager()


    class Meta:

        proxy = True

        verbose_name = "Attendee"

        verbose_name_plural = "Attendees"


    def welcome(self):

        return "Only for Attendee"