from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Contact Messages"
        


class Event(models.Model):
    name = models.CharField(max_length=200)
    organizer = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, )
    venue = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    timestamp = models.DateField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args,**kwargs):
        self.slug = slugify(self.name)
        super(Event,self).save(*args,**kwargs)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.user.username
    

class MailInvites(models.Model):
    subject = models.CharField(max_length=50)
    recipients = models.EmailField(max_length=100)
    message = models.TextField(max_length=500)
    
    class Meta:
        verbose_name_plural = 'Mail invites'
    
    def __unicode__(self):
        return self.name