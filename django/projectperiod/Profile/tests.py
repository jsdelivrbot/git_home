from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from Profile import views
from Core.models import *
from django.conf import settings
from django.contrib.auth import authenticate


class UserSettingsTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.profile = UserProfile(user = self.user, startday = settings.USER_STARTDAY, endday = settings.USER_ENDDAY, steps = settings.USER_STEPS, min_hours = settings.USER_MIN_HOUR, max_hours = settings.USER_MAX_HOUR,
                                                  hourly_rate = settings.USER_HOURLY_RATE, vacation_days = settings.USER_VACATION_DAYS, acquisition = settings.USER_ACQUISITION)
        self.profile.save()

    def test_show_usersettings(self):
        request = self.factory.get('/usersettings/')

        request.user = self.user

        response = views.usersettings(request)
        self.assertEqual(response.status_code, 200)

    def test_modifie_usersettings_user(self):
        request = self.factory.get('/usersettings/')

        request = self.factory.post('/usersettings/', {'firtstname': 'testTest', 'lastname': 'Desc', 'startday': 8, 'endday': 17, 'steps': 5, 'ayquisition': 0, 'email': 'test@daomain.de'})
        request.user = self.user

        response = views.usersettings(request)

        users = len(User.objects.filter(first_name='testTest'))
        self.assertEqual(users, 0)

    def test_modifie_usersettings_profile(self):
        request = self.factory.get('/usersettings/')

        request = self.factory.post('/usersettings/', {'firtstname': 'testTest', 'lastname': 'Desc', 'startday': 3, 'endday': 17, 'steps': 5, 'ayquisition': 0, 'email': 'test@daomain.de'})
        request.user = self.user

        response = views.usersettings(request)

        profiles = len(UserProfile.objects.filter(startday=3))
        self.assertEqual(profiles, 0)


class ChangePasswordTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.user.set_password('testOld')
        self.user.save()
        self.profile = UserProfile(user = self.user, startday = settings.USER_STARTDAY, endday = settings.USER_ENDDAY, steps = settings.USER_STEPS, min_hours = settings.USER_MIN_HOUR, max_hours = settings.USER_MAX_HOUR,
                                                  hourly_rate = settings.USER_HOURLY_RATE, vacation_days = settings.USER_VACATION_DAYS, acquisition = settings.USER_ACQUISITION)
        self.profile.save()

    def test_show_changepassword(self):
        request = self.factory.get('/changepassword/')

        request.user = self.user

        response = views.usersettings(request)
        self.assertEqual(response.status_code, 200)

    def test_changepassword(self):
        request = self.factory.get('/changepassword/')
        loginResult = False

        request = self.factory.post('/changepassword/', {'old': 'testOld', 'new1': 'testNew', 'new2': 'testNew'})
        request.user = self.user

        response = views.changepassword(request)
        userAuth = authenticate(username=self.user.username, password='testNew')
        if userAuth is not None:
            loginResult = True

        self.assertEqual(loginResult, True)

    def test_changepassword_wrong(self):
        request = self.factory.get('/changepassword/')
        loginResult = False

        request = self.factory.post('/changepassword/', {'old': 'testTestWrong', 'new1': 'Desc', 'new2': 8})
        request.user = self.user

        response = views.changepassword(request)
        userAuth = authenticate(username=self.user.username, password='testNew')
        if userAuth is not None:
            loginResult = True

        self.assertEqual(loginResult, False)

class IntegrationsTest(TestCase):
    def setUp(self):
        settings.ROOT_URLCONF = 'Time.urls'
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob', password='top_secret')
        self.customer = Customer(name = 'Intern', street = '-', postcode = '-', city = '-', status = 0)
        self.customer.save()
        self.project = Project(name = 'test', description = '-', status = 1, responsible = self.user, customer = self.customer, billing = 1, budget = 10000, hourly_rate = 100)
        self.project.save()
        self.integration = Integration(user = self.user, tool = 0, project = Project.objects.filter(name='test')[0], url = '-', username = '-', password = '-')
        self.integration.save()

    def test_show_integrations(self):
        request = self.factory.get('/acquisition_counter/')

        request.user = self.user

        response = views.integrations(request)
        self.assertEqual(response.status_code, 200)

    def test_create_integration(self):
        idProject = Project.objects.filter(name='test')[0].id
        request = self.factory.post('/integrations/', {'user': self.user, 'tool': 0, 'project': idProject, 'url': '-', 'username': 'DE', 'password': 0, 'query': '-'})

        request.user = self.user

        response = views.integrations(request)
        integrations = len(Integration.objects.all())

        self.assertEqual(integrations, 2)

    def test_modifie_integration(self):
        idProject = Project.objects.filter(name='test')[0].id
        idIntegration = Integration.objects.all()[0].id
        request = self.factory.post('/integration/', {'action': 'modifie', 'id_integration': idIntegration, 'user': self.user, 'tool': 0, 'project': idProject, 'url': 'http', 'username': 'DE', 'password': 0, 'query': '-'})

        request.user = self.user

        response = views.integration(request)
        integrations = len(Integration.objects.filter(url='http'))
        self.assertEqual(integrations, 1)

    def test_modifie_integration_invalid1(self):
        idProject = Project.objects.filter(name='test')[0].id
        idIntegration = Integration.objects.all()[0].id
        request = self.factory.post('/integration/', {'action': 'modifie', 'id_integration': idIntegration, 'user': self.user, 'tool': 0, 'project': idProject, 'url': 'http', 'username': 'DE'})

        request.user = self.user

        response = views.integration(request)
        integrations = len(Integration.objects.filter(url='http'))
        self.assertEqual(integrations, 0)

    def test_modifie_integration_invalid2(self):
        idProject = Project.objects.filter(name='test')[0].id
        idIntegration = Integration.objects.all()[0].id
        request = self.factory.post('/integration/', {'action': 'modifie', 'id_integration': idIntegration, 'user': self.user, 'tool': 10, 'project': Project.objects.filter(name='test')[0], 'url': 'http', 'username': 'DE', 'password': 0})

        request.user = self.user

        response = views.integration(request)
        integrations = len(Integration.objects.filter(url='http'))
        self.assertEqual(integrations, 0)