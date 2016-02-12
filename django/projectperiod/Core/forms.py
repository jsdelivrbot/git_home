from Crypto.Random.random import choice
from django import forms
from Core.models import *
from django_countries import countries
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms import ModelForm

import datetime

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'street', 'postcode', 'city', 'country', 'customer')
        exclude = ('status',)
        choices = {
            'country': countries.COUNTRIES,
        }

class LocationActiveForm(ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'street', 'postcode', 'city', 'country', 'customer')
        exclude = ('status',)
        choices = {
            'country': countries.COUNTRIES,
        }
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(status = 0), required=True, label=_("Customer"), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'street', 'postcode', 'city', 'country')
        exclude = ('status',)
        choices = {
            'country': countries.COUNTRIES,
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'status', 'responsible', 'customer', 'billing', 'budget', 'hourly_rate')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'responsible': forms.Select(attrs={'class':'form-control'}),
            'customer': forms.Select(attrs={'class':'form-control'}),
            'billing': forms.Select(attrs={'class':'form-control'}),
            'budget': forms.TextInput(attrs={'class':'form-control'}),
            'hourly_rate': forms.TextInput(attrs={'class':'form-control'}),
        }

class ProjectActiveForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'status', 'responsible', 'customer', 'billing', 'budget', 'hourly_rate')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'responsible': forms.Select(attrs={'class':'form-control'}),
            'billing': forms.Select(attrs={'class':'form-control'}),
            'budget': forms.TextInput(attrs={'class':'form-control'}),
            'hourly_rate': forms.TextInput(attrs={'class':'form-control'}),
        }
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(status = 0), required=True, label=_("Customer"), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))

class AcquisitionForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True, input_formats=['%d.%m.%Y'], label=_("Date"), error_messages={'required': _("Please enter a date")})
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(status = 0), required=True, label=_("Customer"), empty_label=None, error_messages={'required': _("A customer is required")}, widget=forms.Select(attrs={'class':'form-control'}))
    project = forms.ModelChoiceField(queryset=Project.objects.filter(status = 1), required=True, label=_("Project"), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))
    location = forms.ModelChoiceField(queryset=Location.objects.filter(status = 0), required=True, label=_("Location"), empty_label=None, error_messages={'required': _("A location is required")},widget=forms.Select(attrs={'class':'form-control'}))
    comment = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255, label=_("Comment"), required=False)
    billable = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'width:100px'}), label=_("Billable"), required=False)
    timeselection = forms.CharField(widget=forms.HiddenInput(), label=_("Time"), required=True, error_messages={'required': _("Please enter a time")})

class AcquisitionCounterForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(status = 0), required=True, label=_("Customer"), empty_label=None, error_messages={'required': _("A customer is required")}, widget=forms.Select(attrs={'class':'form-control'}))
    project = forms.ModelChoiceField(queryset=Project.objects.filter(status = 1), required=True, label=_("Project"), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))
    location = forms.ModelChoiceField(queryset=Location.objects.filter(status = 0), required=True, label=_("Location"), empty_label=None, error_messages={'required': _("A location is required")}, widget=forms.Select(attrs={'class':'form-control'}))
    billable = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'width:100px'}), label=_("Billable"), required=False)
    comment = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255, label=_("Comment"), required=False)

class UserSettingsForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255, label=_("First name"), required=True, error_messages={'required': _("Please enter a first name")})
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255, label=_("Last name"), required=True, error_messages={'required': _("Please enter a last name")})
    startday = forms.ChoiceField(label=_("Daily begin"), choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24')), widget=forms.Select(attrs={'class':'form-control'}))
    endday = forms.ChoiceField(label=_("Daily end"), choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24')), widget=forms.Select(attrs={'class':'form-control'}))
    steps = forms.ChoiceField(label=_("periods"), choices=(('5', '5'), ('6', '6'), ('10', '10'), ('12', '12'), ('15', '15'), ('30', '30')), widget=forms.Select(attrs={'class':'form-control'}))
    acquisition = forms.ChoiceField(label=_("Acquisition"), choices=(('0', 'Explicit'), ('1', 'Counter')), widget=forms.Select(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}), label=_("E-Mail"), required=True, error_messages={'required': _("Please enter an E-Mail")})

class ChangePasswordForm(forms.Form):
    old = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label=_("Old Password"), required=True, error_messages={'required': _("Please enter your old password")})
    new1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label=_("New Password"), required=True, error_messages={'required': _("Please enter your new password")})
    new2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label=_("New Password"), required=True, error_messages={'required': _("Please enter your new password")})

class DateForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}), input_formats=['%d.%m.%Y'], required=True, label=_("Date"), error_messages={'required': _("Please enter a date")})

class DatePeriodForm(forms.Form):
    date1 = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}), input_formats=['%d.%m.%Y'], required=True, label=_("From"), error_messages={'required': _("Please enter a date")})
    date2 = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}), input_formats=['%d.%m.%Y'], required=True, label=_("To"), error_messages={'required': _("Please enter a date")})

class EmployeForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=45, label=_("Username"), required=True, error_messages={'required': _("Please enter an user name")})
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255, label=_("E-Mail"), required=True, error_messages={'required': _("Please enter an E-Mail")})
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255, label=_("First name"), required=True, error_messages={'required': _("Please enter a first name")})
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255, label=_("Last name"), required=True, error_messages={'required': _("Please enter a last name")})
    vacation_days = forms.IntegerField(initial = settings.USER_VACATION_DAYS, widget=forms.TextInput(attrs={'class':'form-control'}), label=_("Vacation days"), required=True, error_messages={'required': _("Please enter vacation days")})
    min_hours = forms.IntegerField(initial = settings.USER_MIN_HOUR, widget=forms.TextInput(attrs={'class':'form-control'}), label=_("Min hours per year"), required=True, error_messages={'required': _("Please enter the min amount of working hours per year")})
    max_hours = forms.IntegerField(initial = settings.USER_MAX_HOUR, widget=forms.TextInput(attrs={'class':'form-control'}), label=_("Max hours per year"), required=True, error_messages={'required': _("Please enter the max amount of working hours per year")})
    hourly_rate = forms.FloatField(initial = settings.USER_HOURLY_RATE, widget=forms.TextInput(attrs={'class':'form-control'}), label=_("Hourly rate"), required=True, error_messages={'required': _("Please enter a hourl rate")})
    management = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'width:100px'}), label=_("Management permission"), required=False)
    api = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'width:100px'}), label=_("API permission"), required=False)

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=255, label=_("E-Mail"), required=True, error_messages={'required': _("Please enter an E-Mail")})

class UserListForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label=_("Username"), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))

class UploadFileForm(forms.Form):
    file  = forms.FileField(label=_("File"))

class YearForm(forms.Form):
    year = forms.ChoiceField(label=_("Year"), choices=((str(x), x) for x in range(2000,datetime.datetime.today().year+1)), widget=forms.Select(attrs={'class':'form-control'}))

class VacationForm(forms.Form):
    date1 = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}), input_formats=['%d.%m.%Y'], required=True, label=_("From"), error_messages={'required': _("Please enter a date")})
    date2 = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}), input_formats=['%d.%m.%Y'], required=True, label=_("To"), error_messages={'required': _("Please enter a date")})
    include_weekend = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'width:100px'}), label=_("Include Weekend"), required=False)

class IntegrationForm(ModelForm):
    class Meta:
        model = Integration
        fields = ('tool', 'project', 'url', 'username', 'password', 'query')
        exclude = ('user',)
        labels = {
            'tool': _("Tool"),
            'url': _("URL"),
            'username': _("Username"),
            'password': _("Password"),
            'query': _("Query"),
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
        }
    project = forms.ModelChoiceField(queryset=Project.objects.filter(status = 1), required=True, label=_("Project"), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))

class BillingForm(ModelForm):
    class Meta:
        model = Billing
    project = forms.ModelChoiceField(queryset=Project.objects.filter(status = 1), required=True, label=_("Project"), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))
    tool = forms.ModelChoiceField(queryset=BillingIntegration.objects.all(), required=True, label=_("Export"), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))


class BillingIntegrationForm(ModelForm):
    class Meta:
        model = BillingIntegration