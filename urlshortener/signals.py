import django.dispatch

shorturl_redirect = django.dispatch.Signal(providing_args=['short_url_id', 'request'])
shorturl_preview  = django.dispatch.Signal(providing_args=['short_url_id', 'request'])
