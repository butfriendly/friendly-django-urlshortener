from django import forms
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_http_methods
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.sites.models import RequestSite
from forms import ShortURLForm
from models import ShortURL
from shortcuts import get_shorturl_or_404
from signals import shorturl_redirect, shorturl_preview

@require_GET
def redirect(request, key):
    short_url = get_shorturl_or_404(key)
    shorturl_redirect.send(sender=None, short_url_id=short_url.id, request=request)
    return HttpResponsePermanentRedirect(short_url.url)

@login_required
@require_http_methods(['GET', 'POST'])
def add(request):
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            short_url = form.save()
            return HttpResponseRedirect(reverse('urlshortener-preview', args=[short_url.key]))
    else:
        if 'u' in request.GET:
            form = ShortURLForm(initial={'url': request.GET['u']})
        else:
            form = ShortURLForm()
    context = {'form': form, 'current_site': RequestSite(request)}
    if request.GET.get('p', False):
        context['base_template'] = 'urlshortener/popup_base.html'
    return render(request, 'urlshortener/add.html', context)

@require_GET
def preview(request, key):
    short_url = get_shorturl_or_404(key)
    shorturl_preview.send(sender=None, short_url_id=short_url.id, request=request)
    return render(request, 'urlshortener/preview.html', {'short_url': short_url, 'current_site': RequestSite(request)})
