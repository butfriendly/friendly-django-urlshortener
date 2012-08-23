from django.http import Http404

from models import ShortURL

def get_shorturl_or_404(key):
    try:
        return ShortURL.objects.get_by_key(key)
    except ShortURL.DoesNotExist:
        raise Http404
