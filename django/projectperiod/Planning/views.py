# Create your views here.
# -*- coding: utf-8 -*- needed for regular expressions with äöü-characters


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission, ContentType
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import *
from django.conf import settings
from django.template import RequestContext
from django_tables2   import RequestConfig
from Core.forms import *
from Core.tables import *
from API.views_api import *
from Core.mail import Mail

import logging
import string
import random


logger = logging.getLogger(__name__)
mail = Mail()

@csrf_exempt
@login_required
@permission_required('auth.management')
def management(request):
    logger.info('function_call management(request) ->')

    c = {'user':request.user, 'standorte': Location.objects.all().count(), 'kunden': Customer.objects.all().count(), 'projekte': Project.objects.all().exclude(name = 'Vacation').exclude(name = 'Ill').count(), 'mitarbeiter': User.objects.all().count(), 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('management.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required('auth.management')
def locations(request):
    logger.info('function_call locations(request) ->')
    
    if request.method == 'POST':
        if request.POST.get('action') == "delete":
            location = Location.objects.get(id = int(request.POST.get('id_record')))
            location.status = 1
            location.save()

            form = LocationActiveForm()
            
        elif request.POST.get('action') == "activate":
            location = Location.objects.get(id = int(request.POST.get('id_record')))
            location.status = 0
            location.save()

            form = LocationActiveForm()
            
        else:
            form = LocationActiveForm(request.POST)
            
            if form.is_valid():
                form.save()
                form = LocationActiveForm()
    else:
        form = LocationActiveForm()

    table = LocationTable(Location.objects.all())
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    c = {'table':table, 'form': form, 'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('locations.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def location(request):
    logger.info('function_call location(request) ->')
    
    if request.method == 'POST':
        location = Location.objects.get(id = int(request.POST.get('id_record')))
        
        form = LocationForm(instance=location)
        
        if request.POST.get('action'):
            if request.POST.get('action') == "modifie":
                form = LocationForm(request.POST, instance=location)
                
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('locations'))
    
    c = {'user':request.user, 'location':location, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('location.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def projects(request):
    logger.info('function_call projects(request) ->')
    
    projects = Project.objects.all().exclude(name = 'Vacation').exclude(name = 'Ill')
    
    if request.method == 'POST':
        form = ProjectActiveForm(request.POST)

        if form.is_valid():
            form.save()
            if form.cleaned_data['status'] == 1:
                project = Project.objects.get(name = form.cleaned_data['name'])
                project.start = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
                project.save()
            if form.cleaned_data['status'] == 2:
                project = Project.objects.get(name = form.cleaned_data['name'])
                project.start = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
                project.end = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
                project.save()

            Membership(user = form.cleaned_data['responsible'], project = Project.objects.get(name = form.cleaned_data['name']), hours = 0).save()
            form = ProjectActiveForm()
    else:
        form = ProjectActiveForm()
    
    table = ProjectTable(projects)
    newtable = ProjectTable(projects.filter(status=0))
    activetable = ProjectTable(projects.filter(status=1))
    closedtable = ProjectTable(projects.filter(status=2))
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    RequestConfig(request).configure(newtable)
    RequestConfig(request).configure(activetable)
    RequestConfig(request).configure(closedtable)

    c = {'table':table, 'newtable':newtable, 'activetable':activetable, 'closedtable':closedtable, 'projects':projects, 'form': form, 'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('projects.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required('auth.management')
def project(request):
    logger.info('function_call project(request) ->')
    
    if request.method == 'POST':
        project = Project.objects.get(id = int(request.POST.get('id_record')))
        
        form = ProjectForm(instance=project)
        
        if request.POST.get('action'):
            if request.POST.get('action') == "modifie":
                form = ProjectForm(request.POST, instance=project)

                if form.is_valid():
                    form.save()

                    if form.cleaned_data['status'] == 1:
                        project = Project.objects.get(id = int(request.POST.get('id_record')))
                        project.start = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
                        project.end = None
                        project.save()
                    if form.cleaned_data['status'] == 2:
                        project = Project.objects.get(id = int(request.POST.get('id_record')))
                        project.end = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
                        project.save()
                    
                    if Membership.objects.filter(user = form.cleaned_data['responsible'], project = project).count() == 0:
                        Membership(user = form.cleaned_data['responsible'], project = project, hours = 0).save()
                    
            if request.POST.get('action') == "remove_staff":
                Membership.objects.get(user = User.objects.get(id=int(request.POST.get('remove_staff'))), project = project).delete()

            if request.POST.get('action') == "budget_staff":
                membership = Membership.objects.get(user = User.objects.get(id=int(request.POST.get('budget_staff'))), project = project)
                membership.hours = int(request.POST.get('budget'))
                membership.save()

            if request.POST.get('action') == "add_staff":
                if Membership.objects.filter(user = User.objects.get(id=int(request.POST.get('add_staff'))), project = project).count() == 0:
                    try:
                        Membership(user = User.objects.get(id=int(request.POST.get('add_staff'))), project = project, hours = int(request.POST.get('budget'))).save()
                    except Exception:
                        Membership(user = User.objects.get(id=int(request.POST.get('add_staff'))), project = project, hours = 0).save()
        
        staff = project.get_staff()
        planned_budget = 0
        
        for personal in staff:
            if int(project.billing) == 1:
                planned_budget = planned_budget + personal.budget * UserProfile.objects.get(user = personal).hourly_rate
            if int(project.billing) == 0:
                planned_budget = planned_budget + personal.budget * project.hourly_rate
        
        
        c = {'project':project, 'form':form, 'users':project.get_unplanned_staff(), 'user':request.user, 'staff':staff, 'planned_budget':planned_budget, 'SITENAME':settings.SITENAME, "currency":settings.CURRENCY, 'management':request.user.has_perm('auth.management')}
        c.update(csrf(request))
        return render_to_response('project.html', c, context_instance=RequestContext(request))
    else:
        c = {'projects':Project.objects.all(), 'form': ProjectForm(), 'user':request.user, 'SITENAME':settings.SITENAME, "currency":settings.CURRENCY, 'management':request.user.has_perm('auth.management')}
        c.update(csrf(request))
        return render_to_response('projects.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def customers(request):
    logger.info('function_call customers(request) ->')
    
    if request.method == 'POST':
        if request.POST.get('action') == "delete":
            customer = Customer.objects.get(id = int(request.POST.get('id_record')))
            customer.status = 1
            customer.save()
            
            form = CustomerForm()
            
        elif request.POST.get('action') == "activate":
            customer = Customer.objects.get(id = int(request.POST.get('id_record')))
            customer.status = 0
            customer.save()
            
            form = CustomerForm()
            
        else:
            form = CustomerForm(request.POST)
            
            if form.is_valid():
                form.save()
                form = CustomerForm()
    else:
        form = CustomerForm()

    table = CustomerTable(Customer.objects.all())
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    c = {'table':table, 'form': form, 'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('customers.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def customer(request):
    logger.info('function_call customer(request) ->')
    
    if request.method == 'POST':
        customer = Customer.objects.get(id = int(request.POST.get('id_record')))
        
        form = CustomerForm(instance=customer)
        
        if request.POST.get('action'):
            if request.POST.get('action') == "modifie":
                form = CustomerForm(request.POST, instance=customer)
                
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('customers'))
    
    c = {'user':request.user, 'customer':customer, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('customer.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def staff(request):
    logger.info('function_call staff(request) ->')

    if request.method == 'POST':
        if request.POST.get('action') == "delete":
            employe = User.objects.get(id = request.POST.get('id_record'))
            employe.is_active = False
            employe.save()
            
            form = EmployeForm()
            
        elif request.POST.get('action') == "activate":
            employe = User.objects.get(id = request.POST.get('id_record'))
            employe.is_active = True
            employe.save()
            
            form = EmployeForm()
            
        else:
            form = EmployeForm(request.POST)

            if form.is_valid():
                pass_size = 6
                password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(pass_size))
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], password)
                user.last_name = form.cleaned_data['lastname']
                user.first_name = form.cleaned_data['firstname']
                user.save()

                userProfile = UserProfile(user = user, startday = 7, endday = 18, steps = 5, min_hours = form.cleaned_data['min_hours'],
                                          max_hours = form.cleaned_data['max_hours'], hourly_rate = form.cleaned_data['hourly_rate'],
                                          vacation_days = form.cleaned_data['vacation_days'], acquisition = settings.USER_ACQUISITION)
                userProfile.save()

                try:
                    permission = Permission.objects.get(codename='management')
                except Exception:
                    permissionNew = Permission(name = "management", content_type = ContentType.objects.get(model='permission'), codename = "management")
                    permissionNew.save()

                permission = Permission.objects.get(codename='management')
                if form.cleaned_data['management'] == True:
                    user.user_permissions.add(permission)
                else:
                    user.user_permissions.remove(permission)

                if form.cleaned_data['api'] == True:
                    user.is_staff = 1
                    user.save()
                else:
                    user.is_staff = 0
                    user.save()
                
                mail.mail_password_new(user, password)

                form = EmployeForm()
    else:
        form = EmployeForm()

    table = StaffTable(User.objects.all())
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    c = {'table':table, 'form':form, 'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('staff.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required('auth.management')
def employe(request):
    logger.info('function_call employe(request) ->')
    
    if request.method == 'POST':
        employe = User.objects.get(id = int(request.POST.get('id_record')))
        profile = UserProfile.objects.get(user = employe)

        form = EmployeForm(initial={'username': employe.username, 'email': employe.email, 'firstname': employe.first_name, 'lastname': employe.last_name,
                                    'vacation_days': profile.vacation_days, 'min_hours': profile.min_hours, 'max_hours': profile.max_hours,
                                    'hourly_rate': profile.hourly_rate, 'management': employe.has_perm('auth.management'), 'api': employe.is_staff})

        if request.POST.get('action'):
            if request.POST.get('action') == "modifie":
                form = EmployeForm(request.POST)
                
                if form.is_valid():
                    employe.username = form.cleaned_data['username']
                    employe.email = form.cleaned_data['email']
                    employe.first_name = form.cleaned_data['firstname']
                    employe.last_name = form.cleaned_data['lastname']
                    employe.save()

                    profile.vacation_days = form.cleaned_data['vacation_days']
                    profile.min_hours = form.cleaned_data['min_hours']
                    profile.max_hours = form.cleaned_data['max_hours']
                    profile.hourly_rate = form.cleaned_data['hourly_rate']
                    profile.save()

                    try:
                        permission = Permission.objects.get(codename='management')
                    except Exception:
                        permissionNew = Permission(name = "management", content_type = ContentType.objects.get(model='permission'), codename = "management")
                        permissionNew.save()

                    permission = Permission.objects.get(codename='management')
                    if form.cleaned_data['management'] == True:
                        employe.user_permissions.add(permission)
                    else:
                        employe.user_permissions.remove(permission)

                    if form.cleaned_data['api'] == True:
                        employe.is_staff = 1
                        employe.save()
                    else:
                        employe.is_staff = 0
                        employe.save()

                    return HttpResponseRedirect(reverse('staff'))

    
    c = {'user':request.user, 'employe':employe, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('employe.html', c, context_instance=RequestContext(request))