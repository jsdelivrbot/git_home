from django.db import models
from django.contrib.auth.models import User
from django_countries import CountryField
from django.utils.translation import ugettext as _
from django.conf import settings

     
class UserProfile(models.Model):
    AQUISITION = (
        (0,'explicit'),
        (1,'counter'),
    )
    user = models.OneToOneField(User)
    startday = models.IntegerField()
    endday = models.IntegerField()
    steps = models.IntegerField()
    min_hours = models.IntegerField()
    max_hours = models.IntegerField()
    hourly_rate = models.FloatField()
    vacation_days = models.IntegerField()
    acquisition = models.IntegerField(choices=AQUISITION)
    def customers(self):
        customers = []
        for membership in Membership.objects.all().filter(user = self.user):
            if membership.project.status == 1:
                if membership.project.customer not in customers:
                    if membership.project.customer.status == 0:
                        customers.append(membership.project.customer)
        return customers
        
    def projects(self):
        projects = []
        for membership in Membership.objects.all().filter(user = self.user):
            if membership.project.status == 1:
                projects.append(membership.project)
        return projects

    def all_projects(self):
        projects = []
        for membership in Membership.objects.all().filter(user = self.user):
            if membership.project.status == 1 or membership.project.status == 2:
                projects.append(membership.project)
        return projects

class Customer(models.Model):
    STATUS = (
        (0,'active'),
        (1,'deactivated'),
    )
    name = models.CharField(max_length=45, unique=True, verbose_name=_('Name'))
    street = models.CharField(max_length=255, verbose_name=_('Street'))
    postcode = models.CharField(max_length=12, verbose_name=_('Postcode'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    country = CountryField(verbose_name=_('Country'))
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=_('Status'))
    def __unicode__(self):
        return self.name
    def projects(self):
        return Project.objects.filter(customer = self).exclude(name = 'Vacation').exclude(name = 'Ill')
    def active_projects(self):
        return Project.objects.filter(customer = self, status = 1)
        
class Project(models.Model):
    STATUS = (
        (0,'New'),
        (1,'Active'),
        (2,'Closed'),
    )
    BILLING = (
        (0,'Consistent hourly wage'),
        (1,'Employe hourly wage'),
    )
    name = models.CharField(max_length=45, unique=True, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    responsible = models.ForeignKey(User, to_field='id', db_column='idresponsible', related_name='project_responsible', verbose_name=_('Responsible'))
    customer = models.ForeignKey(Customer, to_field='id', db_column='idcustomer', related_name='project_customer', verbose_name=_('Customer'))
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=_('Status'))
    budget = models.IntegerField(verbose_name=_('Budget in ' + settings.CURRENCY))
    billing = models.IntegerField(choices=BILLING, verbose_name=_('Billing'))
    hourly_rate = models.FloatField(verbose_name=_('Hourly Rate'))
    staff = models.ManyToManyField(User, through='Membership')
    start = models.DateField(null=True, blank=True, verbose_name=_('Start'))
    end = models.DateField(null=True, blank=True, verbose_name=_('End'))
    def __unicode__(self):
        return self.name
    def get_staff(self):
        return_staff = []
        for user in User.objects.filter(project=self.id):
            user.budget = Membership.objects.get(user = user, project = self).hours
            return_staff.append(user)
        return return_staff
    def get_unplanned_staff(self):
        return_staff = []
        for user in User.objects.all():
            if user not in self.get_staff():
                return_staff.append(user)
        return return_staff
    def consumed(self):
        allAcquisitions = Acquisition.objects.all().filter(project = self)
        consumed = 0
        for ac in allAcquisitions:
            consumed = consumed + (ac.end - ac.start).seconds
        consumed = float("%.2f" % consumed) / 3600
        consumed = float("%.2f" % consumed)
        return consumed
    def employees(self):
        return len(User.objects.filter(project=self.id))
    
class Membership(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    hours = models.IntegerField()
    def consumed(self):
        allAcquisitions = Acquisition.objects.all().filter(project = self.project, user = self.user).exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill'))
        consumed = 0
        for ac in allAcquisitions:
            consumed = consumed + (ac.end.hour*60 + ac.end.minute - ac.start.hour*60 + ac.start.minute ) / 60
        return consumed

class Location(models.Model):
    STATUS = (
        (0,'active'),
        (1,'deactivated'),
    )
    name = models.CharField(max_length=45, unique=True, verbose_name=_('Name'))
    street = models.CharField(max_length=255, verbose_name=_('Street'))
    postcode = models.CharField(max_length=12, verbose_name=_('Postcode'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    country = CountryField(verbose_name=_('Country'))
    customer = models.ForeignKey(Customer, to_field='id', db_column='idcustomer', related_name='location_customer', null=True, blank=True, verbose_name=_('Customer'))
    status = models.IntegerField(choices=STATUS, default=0)
    def __unicode__(self):
        return self.name

class Acquisition(models.Model):
    user = models.ForeignKey(User, to_field='id', db_column='iduser', related_name='acquisition_user')
    start = models.DateTimeField()
    end = models.DateTimeField()
    project = models.ForeignKey(Project, to_field='id', db_column='idproject', related_name='acquisition_project')
    location = models.ForeignKey(Location, to_field='id', db_column='idlocation', related_name='acquisition_location', null=True, blank=True)
    comment = models.CharField(max_length=255)
    billable = models.BooleanField(default=False)
    def customer(self):
        return self.project.customer
    def duration(self):
        return str("%.2f" % float((self.end.hour - self.start.hour + float(self.end.minute - self.start.minute) / 60)))
    def cost(self):
        if self.project.billing == 0:
            return str("%.2f" % float((self.end.hour - self.start.hour + float(self.end.minute - self.start.minute) / 60) * self.project.hourly_rate))
        else:
            rate = UserProfile.objects.get(user = self.user).hourly_rate
            return str("%.2f" % float((self.end.hour - self.start.hour + float(self.end.minute - self.start.minute) / 60) * rate))

class AcquisitionCounter(models.Model):
    user = models.ForeignKey(User, to_field='id', db_column='iduser', related_name='acquisition_counter_user')
    start = models.DateTimeField()
    project = models.ForeignKey(Project, to_field='id', db_column='idproject', related_name='acquisition_counter_project')
    location = models.ForeignKey(Location, to_field='id', db_column='idlocation', related_name='acquisition_counter_location')
    comment = models.CharField(max_length=255)
    billable = models.BooleanField(default=False)
    
class Violation(models.Model):
    TYPE = (
        (0,'pause'),
        (1,'maxhour'),
        (2,'gap'),
        (3,'weekly'),
        (4,'maxhour_year'),
    )
    user = models.ForeignKey(User, to_field='id', db_column='iduser', related_name='violation_user')
    start = models.DateTimeField()
    end = models.DateTimeField()
    pause = models.IntegerField()
    type = models.IntegerField(choices=TYPE)
    deativated = models.BooleanField(default=False)
    def duration(self):
        return str("%.2f" % float((self.end.hour - self.start.hour + float(self.end.minute - self.start.minute) / 60)))

class Integration(models.Model):
    TOOL = (
        (0,'TheBugGenie'),
        (1,'Polarion'),
    )
    user = models.ForeignKey(User, to_field='id', db_column='iduser', related_name='integration_user')
    tool = models.IntegerField(choices=TOOL)
    project = models.ForeignKey(Project, to_field='id', db_column='idproject', related_name='integration_project')
    query = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class BillingIntegration(models.Model):
    TOOL = (
        (0,'CSV'),
        (1,'EMail'),
    )
    tool = models.IntegerField(choices=TOOL, verbose_name=_('Tool'))
    url = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('URL'))
    username = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('Username'))
    password = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('Password'))
    mail = models.EmailField(null=True, blank=True, verbose_name=_('EMail'))
    def __unicode__(self):
        if self.tool == 1:
            return self.get_tool_display() + ': ' + self.mail
        return self.get_tool_display()

class Billing(models.Model):
    TYPE = (
        (0,'All Acquisitions'),
        (1,'Budget'),
        (2,'Billable Acquisitions'),
        (3,'Budget and Billable Acquisitions'),
    )
    project = models.ForeignKey(Project, to_field='id', db_column='idproject', related_name='billing_project', verbose_name=_('Project'))
    tool = models.ForeignKey(BillingIntegration, to_field='id', db_column='idbillingintegration', related_name='billing_integration', verbose_name=_('Tool'))
    start = models.DateField(null=True, blank=True, verbose_name=_('Start'))
    end = models.DateField(null=True, blank=True, verbose_name=_('End'))
    type = models.IntegerField(choices=TYPE, default=0, verbose_name=_('Billing'))