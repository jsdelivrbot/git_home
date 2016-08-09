"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, RequestFactory
from django.conf import settings

from Billing import views
from Core.models import *

import datetime


class BillingTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.customer = Customer(name = 'Intern', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()
        self.project = Project(name = 'test', description = '-', status = 0, responsible = self.user, customer = self.customer, billing = 1, budget = 10000, hourly_rate = 100)
        self.project.save()


    def test_show_billings_denied(self):
        request = self.factory.get('/billing/')

        request.user = self.user

        response = views.billing(request)
        self.assertEqual(response.status_code, 302)

    def test_show_billings(self):
        request = self.factory.get('/billing/')

        self.user.is_superuser = True
        request.user = self.user

        response = views.billing(request)
        self.assertEqual(response.status_code, 200)

    def test_create_billing(self):
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        idProject = Project.objects.get(name = 'test').id
        request = self.factory.post('/billing/', {'project': idProject, 'export': 0, 'billing': 0})

        self.user.is_superuser = True
        request.user = self.user

        response = views.billing(request)
        self.assertEqual(response.status_code, 200)