from django.contrib import admin
from organize.models import Contact, Event, MailInvites

class ContactAdmin(admin.ModelAdmin):
    class Meta:
        model = Contact
        
admin.site.register(Contact, ContactAdmin)

class EventAdmin(admin.ModelAdmin):
    class Meta:
        model = Event
        
class MailIvitesAdmin(admin.ModelAdmin):
    model = MailInvites

admin.site.register(MailInvites, MailIvitesAdmin)
admin.site.register(Event, EventAdmin)
admin.site.site_header = 'E-organizer admin'
        
