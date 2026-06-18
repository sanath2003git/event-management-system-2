from django import forms
from django.utils import timezone

from .models import Event, Booking


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class EventForm(forms.ModelForm):

    class Meta:

        model = Event

        fields = [
            'title',
            'description',
            'date',
            'start_at',
            'end_at',
            'location',
            'image',
            'category'
        ]

        widgets = {

            'date': DateInput(),

            'start_at': TimeInput(),

            'end_at': TimeInput(),
        }

        labels = {

            'title': 'Title',

            'description': 'Description',

            'date': 'Date',

            'start_at': 'Starting time',

            'end_at': 'Ending time',

            'location': 'Location',

            'image': 'Image',

            'category': 'Category',
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.Select):

                field.widget.attrs.update(
                    {
                        'class': 'form-select'
                    }
                )

            else:

                existing_classes = field.widget.attrs.get(
                    'class',
                    ''
                )

                classes = f'{existing_classes} form-control'.strip()

                field.widget.attrs.update(
                    {
                        'class': classes
                    }
                )


class ContactForm(forms.Form):

    name = forms.CharField(

        max_length=100,

        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': 'required',
            }
        )
    )

    email = forms.EmailField(

        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your email address',
                'required': 'required',
            }
        )
    )

    subject = forms.CharField(

        max_length=150,

        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': 'required',
            }
        )
    )

    message = forms.CharField(

        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your message',
                'rows': 5,
                'required': 'required',
            }
        )
    )


class BookingForm(forms.ModelForm):

    event = forms.ModelChoiceField(

        queryset=Event.objects.filter(
            date__gte=timezone.now().date()
        ),

        empty_label="Select an Event",

        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta:

        model = Booking

        fields = ['event']