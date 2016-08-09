from django.contrib.auth.models import User, Group
from Core.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'street', 'postcode', 'city', 'country', 'status')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'responsible', 'customer', 'status', 'budget', 'billing', 'hourly_rate', 'staff')

class AcquisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acquisition
        fields = ('id', 'user', 'start', 'end', 'project', 'location', 'comment', 'billable')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'street', 'postcode', 'city', 'country', 'customer', 'status')