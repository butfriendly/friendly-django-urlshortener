from django.contrib import admin

from models import ShortURL
from forms import ShortURLForm

class ShortURLAdmin(admin.ModelAdmin):
    form = ShortURLForm
    fieldsets = (
        (None, {
            'fields': ('url', 'key')
        }),
    )

    def get_readonly_fields(self, requests, obj=None):
        return ['key', 'url'] if obj else []

admin.site.register(ShortURL, ShortURLAdmin)
