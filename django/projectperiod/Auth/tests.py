from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from Auth import views
from django.conf import settings


class AuthTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')

    def test_login_wrong(self):
        request = self.factory.get('/acquisition_counter/')

        request.user = AnonymousUser()
        request.session = {}

        response = views.login_user(request)
        self.assertEqual(response.status_code, 200)

    def test_login_redirect(self):
        request = self.factory.get('/acquisition_counter/')

        request.user = self.user

        response = views.login_user(request)
        self.assertEqual(response.status_code, 302)