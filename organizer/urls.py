from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$','organize.views.register', name='register'),
    url(r'^login/$', 'organize.views.user_login', name='login'),
    url(r'^logout/$', 'organize.views.user_logout', name='logout'),
    url(r'^$', 'organize.views.index', name='index'),
    url(r'^contact/', 'organize.views.contact', name='contact'),
    url(r'^create_event/$', 'organize.views.create_event', name='create_event'),
    url(r'^events/(?P<slug>[-\w]+)/$', 'organize.views.individual_event', name='events'),
    url(r'^send_mail', 'organize.views.mailer', name='mailer'),
]
