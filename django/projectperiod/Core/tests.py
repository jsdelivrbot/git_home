from random import randint
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from Core import views
from models import *

import requests, json

class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)