from django.conf.urls import patterns, include, url

from models import CHARACTERS
from views import add, redirect, preview

urlpatterns = patterns('',
    url(r'^add/$', add, name='urlshortener-add'),
    url(r'^([%s]+)$'%CHARACTERS, redirect, name='urlshortener-redirect'),
    url(r'^([%s]+)/p$'%CHARACTERS, preview, name='urlshortener-preview'),
)
