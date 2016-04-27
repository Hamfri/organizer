from django import forms
import models
from django.contrib.auth.models import User
from organize.models import Contact, Event, UserProfile, MailInvites

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Your name'}))
    email = forms.EmailField(max_length=500, widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'email eg example@organizer.com'}))
    message = forms.CharField(max_length=1, widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'Message ....'}))
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'venue', 'description', 'start_date', 'end_date']
        exclude = ['organizer',]

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

def get_item():
    events = Event.objects.all()
    item = events.name
    return item

class MailInvitesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailInvitesForm, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.ChoiceField(choices=[(item.id, str(item)) for item in Event.objects.all()], widget=forms.Select(attrs={'class':'form-control'}), required=True)
        self.fields['recipients'] = forms.EmailField(max_length=100, widget=forms.widgets.TextInput(attrs={'class':'form-control','placeholder':'email eg example@organizer.com'}))
        self.fields['message'] = forms.CharField(max_length=500, widget=forms.widgets.Textarea(attrs={'class':'form-control','placeholder':'Message ....'}))
    class Meta:
        model = MailInvites
        fields = ['subject','recipients','message']
    