"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, RequestFactory
from django.conf import settings

from Planning import views
from Core.models import *

import datetime


class ProjectsTest(TestCase):
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


    def test_show_projects_denied(self):
        request = self.factory.get('/acquisition_counter/')

        request.user = self.user

        response = views.projects(request)
        self.assertEqual(response.status_code, 302)

    def test_show_projects(self):
        request = self.factory.get('/acquisition_counter/')

        self.user.is_superuser = True
        request.user = self.user

        response = views.projects(request)
        self.assertEqual(response.status_code, 200)

    def test_create_project(self):
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/projects/', {'name': 'testTest', 'description': 'Desc', 'status': 0, 'responsible': self.user.id, 'customer': idCustomer, 'billing': 0, 'budget': 1000, 'hourly_rate': 100})

        self.user.is_superuser = True
        request.user = self.user

        response = views.projects(request)
        projects = len(Project.objects.all())
        #print(response)
        self.assertEqual(projects, 2)

    def test_create_project_active(self):
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/projects/', {'name': 'testTest', 'description': 'Desc', 'status': 1, 'responsible': self.user.id, 'customer': idCustomer, 'billing': 0, 'budget': 1000, 'hourly_rate': 100})

        self.user.is_superuser = True
        request.user = self.user

        views.projects(request)
        today = datetime.date(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
        project = Project.objects.get(name = 'testTest')
        self.assertEqual(project.start, today)

    def test_create_project_closed(self):
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/projects/', {'name': 'testTest', 'description': 'Desc', 'status': 2, 'responsible': self.user.id, 'customer': idCustomer, 'billing': 0, 'budget': 1000, 'hourly_rate': 100})

        self.user.is_superuser = True
        request.user = self.user

        views.projects(request)
        today = datetime.date(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
        project = Project.objects.get(name = 'testTest')
        self.assertEqual(project.start, today)
        self.assertEqual(project.end, today)

    def test_modifie_project(self):
        idProject = Project.objects.filter(name='test')[0].id
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/project/', {'action': 'modifie', 'id_record': idProject, 'name': 'testTestMod', 'description': 'Desc', 'status': 0, 'responsible': self.user.id, 'customer': idCustomer, 'billing': 0, 'budget': 1000, 'hourly_rate': 100})

        self.user.is_superuser = True
        request.user = self.user

        response = views.project(request)
        projects = len(Project.objects.filter(name='testTestMod'))
        self.assertEqual(projects, 1)

    def test_modifie_project_invalid1(self):
        idProject = Project.objects.filter(name='test')[0].id
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/project/', {'action': 'modifie', 'id_record': idProject, 'name': 'testTestMod', 'status': 0, 'responsible': self.user.id, 'customer': idCustomer, 'billing': 0, 'budget': 1000, 'hourly_rate': 100})

        self.user.is_superuser = True
        request.user = self.user

        response = views.project(request)
        projects = len(Project.objects.filter(name='testTestMod'))
        self.assertEqual(projects, 0)

    def test_modifie_project_invalid2(self):
        idProject = Project.objects.filter(name='test')[0].id
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/project/', {'action': 'modifie', 'id_record': idProject, 'name': 'testTestMod', 'description': 'Desc', 'status': 10, 'responsible': self.user.id, 'customer': idCustomer, 'billing': 0, 'budget': 1000, 'hourly_rate': 100})

        self.user.is_superuser = True
        request.user = self.user

        response = views.project(request)
        projects = len(Project.objects.filter(name='testTestMod'))
        self.assertEqual(projects, 0)

class LocationsTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.customer = Customer(name = 'Intern', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()
        self.location = Location(name = 'test', street = '-', postcode = '12345', city = '-', country = 'DE', customer = self.customer, status = 0)
        self.location.save()

    def test_show_locations_denied(self):
        request = self.factory.get('/acquisition_counter/')

        request.user = self.user

        response = views.locations(request)
        self.assertEqual(response.status_code, 302)

    def test_show_locations(self):
        request = self.factory.get('/acquisition_counter/')

        self.user.is_superuser = True
        request.user = self.user

        response = views.locations(request)
        self.assertEqual(response.status_code, 200)

    def test_create_location(self):
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/locations/', {'name': 'testTest', 'street': '-', 'postcode': '12345', 'city': '-', 'country': 'DE', 'customer': idCustomer, 'status': 0})

        self.user.is_superuser = True
        request.user = self.user

        response = views.locations(request)
        locations = len(Location.objects.all())
        #print(response)
        self.assertEqual(locations, 2)

    def test_modifie_location(self):
        idLocation = Location.objects.filter(name='test')[0].id
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/location/', {'action': 'modifie', 'id_record': idLocation, 'name': 'testTestMod', 'street': '-', 'postcode': '12345', 'city': '-', 'country': 'DE', 'customer': idCustomer, 'status': 0})

        self.user.is_superuser = True
        request.user = self.user

        response = views.location(request)
        locations = len(Location.objects.filter(name='testTestMod'))
        self.assertEqual(locations, 1)

    def test_modifie_location_invalid1(self):
        idLocation = Location.objects.filter(name='test')[0].id
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/location/', {'action': 'modifie', 'id_record': idLocation, 'name': 'testTest', 'postcode': '12345', 'city': '-', 'country': 'DE', 'customer': idCustomer, 'status': 0})

        self.user.is_superuser = True
        request.user = self.user

        response = views.location(request)
        locations = len(Location.objects.filter(name='testTestMod'))
        self.assertEqual(locations, 0)

    def test_modifie_location_invalid2(self):
        idLocation = Location.objects.filter(name='test')[0].id
        idCustomer = Customer.objects.filter(name='Intern')[0].id
        request = self.factory.post('/location/', {'action': 'modifie', 'id_record': idLocation, 'name': 'testTest', 'street': '-', 'postcode': '12345', 'city': '-', 'country': 'DE', 'customer': idCustomer, 'status': 10})

        self.user.is_superuser = True
        request.user = self.user

        response = views.location(request)
        locations = len(Location.objects.filter(name='testTestMod'))
        self.assertEqual(locations, 0)

class CustomersTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.customer = Customer(name = 'test', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()

    def test_show_customers_denied(self):
        request = self.factory.get('/acquisition_counter/')

        request.user = self.user

        response = views.customers(request)
        self.assertEqual(response.status_code, 302)

    def test_show_customers(self):
        request = self.factory.get('/acquisition_counter/')

        self.user.is_superuser = True
        request.user = self.user

        response = views.customers(request)
        self.assertEqual(response.status_code, 200)

    def test_create_customer(self):
        idCustomer = Customer.objects.filter(name='test')[0].id
        request = self.factory.post('/customers/', {'name': 'testTest', 'street': '-', 'postcode': '12345', 'city': '-', 'country': 'DE', 'status': 0})

        self.user.is_superuser = True
        request.user = self.user

        response = views.customers(request)
        customers = len(Customer.objects.all())
        #print(response)
        self.assertEqual(customers, 2)

    def test_modifie_customer(self):
        idCustomer = Customer.objects.filter(name='test')[0].id
        request = self.factory.post('/customer/', {'action': 'modifie', 'id_record': idCustomer, 'name': 'testTestMod', 'street': '-', 'postcode': '12345', 'city': '-', 'country': 'DE', 'status': 0})

        self.user.is_superuser = True
        request.user = self.user

        response = views.customer(request)
        customers = len(Customer.objects.filter(name='testTestMod'))
        self.assertEqual(customers, 1)

    def test_modifie_customer_invalid1(self):
        idCustomer = Customer.objects.filter(name='test')[0].id
        request = self.factory.post('/customer/', {'action': 'modifie', 'id_record': idCustomer, 'name': 'testTest', 'postcode': '12345', 'city': '-', 'country': 'DE', 'status': 0})

        self.user.is_superuser = True
        request.user = self.user

        response = views.customer(request)
        customers = len(Customer.objects.filter(name='testTestMod'))
        self.assertEqual(customers, 0)

    def test_modifie_customer_invalid2(self):
        idCustomer = Customer.objects.filter(name='test')[0].id
        request = self.factory.post('/customer/', {'action': 'modifie', 'id_record': idCustomer, 'name': 'testTest', 'street': '-', 'postcode': '12345', 'city': '-', 'country': 'DE', 'status': 10})

        self.user.is_superuser = True
        request.user = self.user

        response = views.customer(request)
        customers = len(Customer.objects.filter(name='testTestMod'))
        self.assertEqual(customers, 0)