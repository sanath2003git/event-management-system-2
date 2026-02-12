# In forms.py

# from django import forms
# from .models import Event

# class DateInput(forms.DateInput):
#     input_type='date'

# class TimeInput(forms.TimeInput):
#     input_type='time'

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = '__all__'

#         widgets={
#             'date' : DateInput(),
#             'start_at' : TimeInput(),
#             'end_at' : TimeInput(),
#         }

#         labels={
#             'title' : 'Title',
#     'description' : 'Description',
#     'date' : 'Date',
#     'start_at' : 'Starting time',
#     'end_at' : 'Ending time',
#     'location' : 'Location',
#     'image' : 'Image',
#         }


from django import forms
from .models import Event,Booking

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # Only include fields the organizer should fill
        fields = ['title', 'description', 'date', 'start_at', 'end_at', 'location', 'image','category']
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
        super(EventForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add Bootstrap classes to widgets
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                # For date/time/text inputs, add form-control
                existing_classes = field.widget.attrs.get('class', '')
                classes = f'{existing_classes} form-control'.strip()
                field.widget.attrs.update({'class': classes})


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your full name',
        'required': 'required',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your email address',
        'required': 'required',
    }))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject',
        'required': 'required',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Your message',
        'rows': 5,
        'required': 'required',
    }))


class BookingForm(forms.ModelForm):
    # Limit event choices to future events or all, adjust as needed
    event = forms.ModelChoiceField(queryset=Event.objects.all(), empty_label="Select an Event")

    class Meta:
        model = Booking
        fields = ['event']    