"""

    >>> s1 = ShortURL(url='http://example.com/a')
    >>> s1.save()
    >>> s1.id
    1

IDs can be sparse, holes will be filled.

    >>> s3 = ShortURL(url='http://example.com/c', id=3)
    >>> s3.save()
    >>> s3.id
    3
    >>> s2 = ShortURL(url='http://example.com/b')
    >>> s2.save()
    >>> s2.id
    2
    >>> s4 = ShortURL(url='http://example.com/d')
    >>> s4.save()
    >>> s4.id
    4
    >>> s5 = ShortURL(url='http://example.com/e', id=6)
    >>> s5.save()
    >>> s5.id
    6
    >>> s6 = ShortURL(url='http://example.com/f')
    >>> s6.save()
    >>> s6.id
    5
    >>> s7 = ShortURL(url='http://example.com/g')
    >>> s7.save()
    >>> s7.id
    7
"""

import string
from django.db import models
from django.db import connection, transaction
from django.conf import settings
from django.contrib.sites.models import Site

DEFAULT_CHARACTERS = string.digits + string.ascii_letters
DEFAULT_BLACKLIST = ['admin', 'add']

class ShortURLManager(models.Manager):

    last_id = 0

    def get_next_id(self, last_id=None):
        if last_id is None:
            last_id = self.last_id
        cursor = connection.cursor()
        cursor.execute('''
            SELECT  id + 1
            FROM    urlshortener_shorturl mo
            WHERE   id >= %s
            AND     NOT EXISTS
                    (
                    SELECT  NULL
                    FROM    urlshortener_shorturl mi 
                    WHERE   mi.id = mo.id + 1
                    )
            ORDER BY id ASC
            LIMIT 1
        '''%last_id)
        row = cursor.fetchone()
        next_id = row[0] if row else 1
        # make sure we don't return a blacklisted id
        while next_id in BLACKLIST:
            self.get_next_id(next_id)
        self.last_id = next_id
        return next_id

    def create_with_key(self, key):
        kwargs['id'] = key_to_id(kwargs)
        return self.create(**kwargs)

    def get_by_key(self, key):
        return self.get(id=key_to_id(key))

class ShortURL(models.Model):
    id  = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

    def _get_key(self): return id_to_key(self.id) if self.id else ''
    def _set_key(self, key): self.id = key_to_id(key)
    key = property(_get_key, _set_key)

    objects = ShortURLManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = ShortURL.objects.get_next_id()
        super(ShortURL, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s <%s>'%(id_to_key(self.id or 0), self.url)

def key_to_id(key):
    """
    Turns a key into an integer.

        >>> key_to_id('1')
        1
        >>> key_to_id('a')
        10
        >>> key_to_id('10')
        62
    """
    n = len(CHARACTERS)
    id = 0
    for c in key:
        id *= n
        id += CHARACTERS.index(c)
    return id

def id_to_key(key):
    """
    Turns an integer into a key.

        >>> id_to_key(1)
        '1'
        >>> id_to_key(10)
        'a'
        >>> id_to_key(62)
        '10'
    """
    if key == 0: return '0'
    digits = []
    n = len(CHARACTERS)
    while key > 0:
        digits.append(CHARACTERS[key % n])
        key /= n
    return ''.join(reversed(digits))

CHARACTERS = getattr(settings, 'URLSHORTENER_CHARACTERS', DEFAULT_CHARACTERS)
blacklisted = getattr(settings, 'URLSHORTENER_BLACKLIST', DEFAULT_BLACKLIST)
BLACKLIST = dict((key_to_id(key), True) for key in blacklisted)
