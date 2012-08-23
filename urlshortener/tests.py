from urlparse import urlparse

from django.test import TestCase
from django.core.urlresolvers import resolve

from models import ShortURL

class ShortURLTest(TestCase):

    fixtures = ['urlshortener/super_user.json']

    def test_add(self):
        """
        Tests adding of a Short URL.
        """
        self.client.login(username='admin', password='admin')
        response = self.client.post('/add/', {'url': 'http://example.com'}, follow=True)
        self.assertShortURLCreated(response)

    def test_add_with_key(self):
        """
        Tests adding of a Short URL with a custom key.
        """
        self.client.login(username='admin', password='admin')
        response = self.client.post('/add/', {'url': 'http://example.com', 'key': 'example'}, follow=True)
        self.assertShortURLCreated(response, 'example')

    def assertShortURLCreated(self, response, expected_key=None):
        self.assertEqual(response.redirect_chain[0][1], 302)
        print response.redirect_chain
        self.assertEqual(response.status_code, 200)
        path = urlparse(response.redirect_chain[0][0]).path
        match = resolve(path)
        key = match.args[0]
        self.assertTrue(ShortURL.objects.get_by_key(key))
        if expected_key is not None:
            self.assertEqual(expected_key, key)

    def test_add_with_existing_key(self):
        """
        Tests adding of a Short URL with a custom key that already exists.
        """
        self.client.login(username='admin', password='admin')
        response = self.client.post('/add/', {'url': 'http://example.com', 'key': 'example'})
        # TODO status 201
        self.client.login(user='admin', password='admin')
        response = self.client.post('/add/', {'url': 'http://example.com', 'key': 'example'})
        # TODO status 409

    def test_unauthorized_add(self):
        """
        Tests adding of a Short URL without being authorized.
        """
        response = self.client.post('/add/', {'url': 'http://example.com', 'key': 'example'})
        # TODO status 403
        

    def test_forward(self):
        """
        Tests forwarding of a Short URL
        """
        short_url = ShortURL.objects.create(url='http://example.com')
        response = self.client.get('/%s'%(short_url.key))
        self.assertEqual(response.status_code, 301)
