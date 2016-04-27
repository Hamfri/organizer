from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from smtplib import SMTPException

from organize.forms import ContactForm, EventForm, UserProfileForm, MailInvitesForm
from organize.models import Event, MailInvites

@login_required
def index(request):
    events = Event.objects.all()
    if len(events) == 0:
        messages.add_message(request, messages.ERROR, 'No events are added currently')
    return render(request,'index.html',locals())

def individual_event(request,slug):
    single_event = Event.objects.get(slug=slug)
    return render(request, 'single_event.html', locals())

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.add_message(request, messages.INFO, 'Your message has been sent Successfully'
                                 )
            return HttpResponseRedirect('/')
        else:
            print form.errors
    else:
        form = ContactForm()        
    return render(request, 'contact.html', locals())

@login_required
def create_event(request):
    field_class = ['name', 'venue', 'description', 'start_date','end_date']
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.organizer = request.user
            post.save()
            messages.add_message(request, messages.INFO, 'Event Created Successfully{0}'.format(request.user))
            return HttpResponseRedirect('/')
        else:
            print form.errors
    else:
        form = EventForm()
    for key in form.fields.keys():
        if key in field_class:
            field = form.fields[key]
            field.widget.attrs['class'] = 'form-control'
    return render(request, 'create_event.html', locals())

def register(request):
    field_class = ('username', 'email', 'password')
    registered = False
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        else:
            print user_form.errors
    else:
        user_form = UserProfileForm()
    for key in user_form.fields.keys():
        if key in field_class:
            field = user_form.fields[key]
            field.widget.attrs['class'] = 'form-control'
        
    return render(request, 'register.html', locals())


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.INFO, 'Your account is disabled')
        else:
            print "Invalid login details: {0}, {1}".format(username,password)
            messages.add_message(request, messages.INFO, 'Invalid login details')
            return HttpResponseRedirect("/login")
    else:
        return render(request, 'login.html', locals())
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def mailer(request):
    form = MailInvitesForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        recipients = cd['recipients']
        subject = cd['subject']
        message = cd['message']
        if subject and message and recipients:
            try:
                send_mail(subject, message, None, [recipients,], fail_silently=False)
                messages.add_message(request, messages.SUCCESS, 'Email sent successfully')
                return redirect('/')
            except BadHeaderError:
                form.save()
    return render(request, 'mailer.html', locals())
