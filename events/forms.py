from django import forms
from betterforms.multiform import MultiModelForm
from django.contrib.auth.models import User

from .models import Event, EventImage, EventAgenda, AdminMessage, EventComment


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['category', 'name', 'description', 'scheduled_status', 'venue', 'start_date', 'end_date', 'location', 'points', 'maximum_attende', 'status']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        print(f"EventForm cleaned_data: {cleaned_data}")
        return cleaned_data


class EventImageForm(forms.ModelForm):


    class Meta:
        model = EventImage
        fields = ['image']



class EventAgendaForm(forms.ModelForm):


    class Meta:
        model = EventAgenda
        fields = ['start_time', 'end_time', 'venue_name']

        widgets = {
            'start_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class EventCreateMultiForm(MultiModelForm):
    form_classes = {
        'event': EventForm,
        'event_image': EventImageForm,
        'event_agenda': EventAgendaForm,
    }


class AdminMessageForm(forms.ModelForm):
    """Form for users to send messages to administrators"""
    class Meta:
        model = AdminMessage
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the subject of your message',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter your message here...',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.sender = self.user
            instance.sender_email = self.user.email
        if commit:
            instance.save()
        return instance


class AdminMessageResponseForm(forms.ModelForm):
    """Form for administrators to respond to user messages"""
    class Meta:
        model = AdminMessage
        fields = ['response', 'status']
        widgets = {
            'response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter your response...'
            }),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


class EventCommentForm(forms.ModelForm):
    """Form for users to comment on events"""
    class Meta:
        model = EventComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts about this event...',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.event = kwargs.pop('event', None)
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if self.event:
            instance.event = self.event
        if self.parent:
            instance.parent = self.parent
        if commit:
            instance.save()
        return instance


class ContactForm(forms.Form):
    """Form for anonymous users to contact admins"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address',
            'required': True
        })
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject',
            'required': True
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Your message...',
            'required': True
        })
    )