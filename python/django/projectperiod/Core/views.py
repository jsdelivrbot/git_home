# Create your views here.
# -*- coding: utf-8 -*- needed for regular expressions with äöü-characters


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import *
from django.conf import settings
from django.template import RequestContext
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext as _
import logging
import string
import random
import csv

from Core.mail import Mail
from Core.query import Query
from Core.forms import *
from API.views_api import *


logger = logging.getLogger(__name__)
mail = Mail()

class EntrieClass:
    hour = ""
    min = ""
    active = True
    def __init__(self, hour, min, active):
        self.hour = hour
        self.min = min
        self.active = active

@csrf_exempt
@login_required
def index_redirect(request):
    logger.info('function_call index_redirect(request) ->')

    c = {'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return HttpResponseRedirect(reverse('acquisition'))

@csrf_exempt
@login_required
def acquisition(request):
    logger.info('function_call acquisition(request) ->')

    profile = UserProfile.objects.get(user = request.user)
    counter = AcquisitionCounter.objects.filter(user = request.user)

    if counter.count() > 0:
        c = {'Start':counter[0].start, 'Project':counter[0].project, 'Location':counter[0].location, 'Comment':counter[0].comment, 'user':request.user,'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
        c.update(csrf(request))
        return render_to_response('acquisition_counter_stop.html', c, context_instance=RequestContext(request))

    if profile.acquisition == 0:
        return HttpResponseRedirect(reverse('acquisition_explicit'))
    else:
        return HttpResponseRedirect(reverse('acquisition_counter'))

@csrf_exempt
@login_required
def acquisition_explicit(request):
    logger.info('function_call acquisition_explicit(request) ->')

    projects = UserProfile.objects.get(user = request.user).projects()

    if len(projects) == 0:
        c = {'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
        c.update(csrf(request))
        return render_to_response('acquisition_empty.html', c, context_instance=RequestContext(request))

    userProfile = UserProfile.objects.get(user=request.user)
    starthour = userProfile.startday
    endhour = userProfile.endday
    minsteps = userProfile.steps
    today = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, 0, 9)
    customers = UserProfile.objects.get(user = request.user).customers()
    customer = ''
    #projects = customers[0].active_projects()

    if request.method == 'POST':
        if request.POST.get('chooseddate') or request.POST.get('choosedcustomer'):
            try:
                today = datetime.datetime.strptime(request.POST.get('chooseddate'), '%d.%m.%Y')
            except Exception:
                1+1
            customer = Customer.objects.get(id = int(request.POST.get('choosedcustomer')))
            projects = customer.active_projects()
            form = AcquisitionForm()
        elif request.POST.get('expand'):
            today = datetime.datetime(int(request.POST.get('chooseddate_expand').split(".")[2]), int(request.POST.get('chooseddate_expand').split(".")[1]), int(request.POST.get('chooseddate_expand').split(".")[0]))
            form = AcquisitionForm()
            starthour = 0
            endhour = 24
        else:
            form = AcquisitionForm(request.POST)
            form.date = datetime.datetime.strptime(request.POST.get('date'), '%d.%m.%Y').date   #TODO check to optimize
            form.customer = request.POST.get('customer')
            form.project = request.POST.get('project')
            form.location = request.POST.get('location')
            form.comment = request.POST.get('comment')
            form.timeselection = request.POST.get('timeselection')
            form.billable = request.POST.get('billable')

            if form.is_valid():
                today = datetime.datetime(int(request.POST.get('date').split(".")[2]), int(request.POST.get('date').split(".")[1]), int(request.POST.get('date').split(".")[0]))
                timesplit = form.timeselection.split("#")
                start = ''
                end = datetime.time(0, 0)

                for time in timesplit:
                    if time != '':
                        if start == '':
                            start = datetime.time(int(time.split(":")[0]), int(time.split(":")[1]))
                        diff = datetime.time(int(time.split(":")[0]), int(time.split(":")[1]))

                        if end == diff or end == datetime.time(0, 0):
                            if int(time.split(":")[1])+minsteps > 59:
                                end = datetime.time(int(time.split(":")[0])+1, 0)
                            else:
                                end = datetime.time(int(time.split(":")[0]), int(time.split(":")[1])+minsteps)
                        else:
                            startdate = datetime.datetime(form.cleaned_data['date'].year,form.cleaned_data['date'].month,form.cleaned_data['date'].day, start.hour, start.minute)
                            enddate = datetime.datetime(form.cleaned_data['date'].year,form.cleaned_data['date'].month,form.cleaned_data['date'].day, end.hour, end.minute)
                            acquisition = Acquisition(user = request.user, project = Project.objects.get(id = form.project), location = form.cleaned_data['location'], comment = form.cleaned_data['comment'], start = startdate, end = enddate, billable = form.cleaned_data['billable'])
                            acquisition.save()
                            start = datetime.time(int(time.split(":")[0]), int(time.split(":")[1]))
                            if int(time.split(":")[1])+minsteps > 59:
                                end = datetime.time(int(time.split(":")[0])+1, 0)
                            else:
                                end = datetime.time(int(time.split(":")[0]), int(time.split(":")[1])+minsteps)

                startdate = datetime.datetime(form.cleaned_data['date'].year,form.cleaned_data['date'].month,form.cleaned_data['date'].day, start.hour, start.minute)
                enddate = datetime.datetime(form.cleaned_data['date'].year,form.cleaned_data['date'].month,form.cleaned_data['date'].day, end.hour, end.minute)
                acquisition = Acquisition(user = request.user, project = Project.objects.get(id = form.project), location = form.cleaned_data['location'], comment = form.cleaned_data['comment'], start = startdate, end = enddate, billable = form.cleaned_data['billable'])
                acquisition.save()

                form = AcquisitionForm()
    else:
        form = AcquisitionForm()

    entries = []
    delta = datetime.timedelta(days=1)
    acquised = Acquisition.objects.all().filter(user=request.user, end__range=(today, today+delta))

    for hour in range(starthour,endhour):
        for minute in range(00,60,minsteps):
            active = True
            for ac in acquised:
                if datetime.time(ac.start.hour, ac.start.minute) <= datetime.time(hour, minute) < datetime.time(ac.end.hour, ac.end.minute):
                    active = False
                if ac.project == Project.objects.get(name='Vacation') or ac.project == Project.objects.get(name='Ill'):
                    if ac.end != today:
                        active = False
            entries.append(EntrieClass(hour, minute, active))

    #c = {'form':form, 'customers':customers, 'user':request.user, 'hourArray':range(starthour,endhour), 'minArray':range(00,60,minsteps), 'entries':Acquisition.objects.all().filter(user=request.user, end__range=(datetime.datetime(today.year, today.month, today.day), datetime.datetime(today.year, today.month, today.day+1)))}
    c = {'form':form, 'user':request.user, 'entries':entries, 'today':today, 'customers':customers, 'activcustomer':customer, 'projects':projects, 'last':60-minsteps, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('acquisition.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def acquisition_counter(request):
    logger.info('function_call acquisition_counter(request) ->')

    projects = UserProfile.objects.get(user = request.user).projects()

    if len(projects) == 0:
        c = {'user':request.user,'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
        c.update(csrf(request))
        return render_to_response('acquisition_empty.html', c, context_instance=RequestContext(request))

    userProfile = UserProfile.objects.get(user=request.user)
    starthour = userProfile.startday
    endhour = userProfile.endday
    minsteps = userProfile.steps
    today = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
    customers = UserProfile.objects.get(user = request.user).customers()
    customer = ''
    projects = customers[0].active_projects()
    counter = AcquisitionCounter.objects.filter(user = request.user)

    if request.method == 'POST':
        if request.POST.get('choosedcustomer'):
            customer = Customer.objects.get(id = int(request.POST.get('choosedcustomer')))
            projects = customer.active_projects()
            form = AcquisitionCounterForm()
        elif request.POST.get('stop'):
            now = datetime.datetime.today()
            now = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute) + datetime.timedelta(minutes=1)
            acquisition = Acquisition(user = request.user, project = counter[0].project, location = counter[0].location, comment = counter[0].comment, start = counter[0].start, end = now, billable = counter[0].billable)
            acquisition.save()
            counter[0].delete()
            return HttpResponseRedirect(reverse('acquisition'))
        else:
            form = AcquisitionCounterForm(request.POST)

            if form.is_valid():
                now = datetime.datetime.today()
                now = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
                acquisitionCounter = AcquisitionCounter(user = request.user, project = form.cleaned_data['project'], location = form.cleaned_data['location'], comment = form.cleaned_data['comment'], start = now, billable = form.cleaned_data['billable'])
                acquisitionCounter.save()

                c = {'Start':now, 'Project':form.cleaned_data['project'], 'Location':form.cleaned_data['location'], 'Comment':form.cleaned_data['comment'], 'user':request.user,'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
                c.update(csrf(request))
                return render_to_response('acquisition_counter_stop.html', c, context_instance=RequestContext(request))
    else:
        if counter.count() > 0:
            c = {'Start':counter[0].start, 'Project':counter[0].project, 'Location':counter[0].location, 'Comment':counter[0].comment, 'user':request.user,'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
            c.update(csrf(request))
            return render_to_response('acquisition_counter_stop.html', c, context_instance=RequestContext(request))

        form = AcquisitionCounterForm()

    c = {'form':form, 'user':request.user, 'today':today, 'customers':customers, 'activcustomer':customer, 'projects':projects, 'selectionwidth':3600/minsteps, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('acquisition_counter.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def overview_day(request):
    logger.info('function_call overview_day(request) ->')

    today = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)

    if request.POST.get('action'):
            if request.POST.get('action') == "delete":
                entry = Acquisition.objects.get(id=request.POST.get('id_entry'))
                entry.delete()
            if request.POST.get('action') == "choosedate":
                try:
                    today = datetime.datetime.strptime(request.POST.get('date'), '%d.%m.%Y')
                except Exception:
                    1+1

    queryresult = Query().overview_day(request.user, today)
    
    c = {'user':request.user, 'form':DateForm(), 'today':today, 'start':queryresult['start'], 'end':queryresult['end'], 'break':queryresult['breakstring'], 'entire':queryresult['entirestring'], 'entries':queryresult['allAcquisitions'], 'projects':queryresult['projects'], 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('overview_day.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def overview_week(request):
    logger.info('function_call overview_week(request) ->')
    
    days = Query().overview_week(request.user, datetime.datetime.today())
    
    c = {'user':request.user, 'days':days, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('overview_week.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def overview_month(request):
    logger.info('function_call overview_month(request) ->')
    
    date = datetime.datetime.today()
    
    if request.POST.get('date'):
        date = datetime.datetime.strptime(request.POST.get('date'), '%m.%Y')
    
    days = Query().overview_month(request.user, date.month, date.year)
    
    c = {'user':request.user, 'days':days, 'date':date, 'date_left':date - relativedelta( months = +1 ), 'date_right':date + relativedelta( months = +1 ), 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('overview_month.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def overview_year(request):
    logger.info('function_call overview_year(request) ->')
    
    year = datetime.datetime.today().year
    
    if request.POST.get('year'):
        year = int(request.POST.get('year'))
    
    months = Query().overview_year(request.user, year)
    
    c = {'user':request.user, 'months':months, 'year':year, 'year_left':year - 1, 'year_right':year + 1, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('overview_year.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def personal_budget(request):
    logger.info('function_call personal_budget(request) ->')

    year = datetime.datetime.today().year
    form = YearForm(initial={'year':year})

    if request.method == 'POST':
        form = YearForm(request.POST)

        if form.is_valid():
            year = int(form.cleaned_data['year'])

    percent_yellow = 0
    percent_red = 0
    projects = UserProfile.objects.get(user = request.user).all_projects()
    worked = 0
    allAcquisitions = Acquisition.objects.all().filter(user=request.user)
    userProfile = UserProfile.objects.get(user = request.user)

    expected = '-'
    if year == datetime.datetime.today().year:
        average = Query().average_hours(request.user, year)
        if average > 0:
            expected = average * (250 - userProfile.vacation_days) / 60
    
    for project in projects:
        project.consumed = 0
        project.consumed_all = 0
        project.my_hours = Membership.objects.get(user = request.user, project = project).hours
        
        for ac in allAcquisitions:
            if ac.project == project:
                project.consumed_all = project.consumed_all + (ac.end - ac.start).seconds
                if ac.start.date().year == year:
                    project.consumed = project.consumed + (ac.end - ac.start).seconds
                    worked = worked + (ac.end - ac.start).seconds
        project.consumed_all = float("%.2f" % project.consumed_all) / 3600
        project.consumed_all = float("%.2f" % project.consumed_all)
        project.consumed = float("%.2f" % project.consumed) / 3600
        project.consumed = float("%.2f" % project.consumed)
    worked = float("%.2f" % worked) / 3600

    if worked < userProfile.min_hours:
        percent_green = worked * 100 / userProfile.max_hours + 1
    elif worked < userProfile.max_hours:
        percent_green  = userProfile.min_hours * 100 / userProfile.max_hours + 1
        percent_yellow = worked * 100 / userProfile.max_hours - percent_green
    else:
        percent_red = int(100 - (userProfile.max_hours * 100 / worked))
        percent_green  = userProfile.min_hours * (100-percent_red) / userProfile.max_hours + 1
        percent_yellow = (userProfile.max_hours - userProfile.min_hours) * (100-percent_red) / userProfile.max_hours


    c = {'user':request.user, 'worked':float("%.2f" % worked), 'userProfile':userProfile, 'projects': projects, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management'), 'percent_green':int(percent_green), 'percent_yellow':int(percent_yellow), 'percent_red':int(percent_red), 'expected':expected, 'form':form}
    c.update(csrf(request))
    return render_to_response('personal_budget.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def vacation(request):
    logger.info('function_call vacation(request) ->')

    msg = []
    error = []
    form = VacationForm()
    today = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
    allAcquisitions = Acquisition.objects.all().filter(user=request.user, project = Project.objects.get(name='Vacation'))

    if request.method == 'POST':
        if request.POST.get('action') == "add":
            form = VacationForm(request.POST)

            if form.is_valid():
                date1 = form.cleaned_data['date1']
                date2 = form.cleaned_data['date2']
                if date1 < date2:
                    while date1 <= date2:
                        if form.cleaned_data['include_weekend'] == False:
                            if date1.isoweekday() == 6 or date1.isoweekday() == 7:
                                date1 = date1 + datetime.timedelta(days=1)
                                continue
                        if allAcquisitions.filter(start=date1):
                            error.append(_('Already planned vacation for: ') + str(date1))
                            date1 = date1 + datetime.timedelta(days=1)
                            continue
                        acquisition = Acquisition(user = request.user, project = Project.objects.get(name = 'Vacation'), comment = '', start = date1, end = date1 + datetime.timedelta(days=1))
                        acquisition.save()
                        date1 = date1 + datetime.timedelta(days=1)
                        msg.append(_('Planned vacation for: ') + str(date1))

                elif date1 == date2:
                    if not allAcquisitions.filter(start=date1):
                        acquisition = Acquisition(user = request.user, project = Project.objects.get(name = 'Vacation'), comment = '', start = date1, end = date1 + datetime.timedelta(days=1))
                        acquisition.save()
                        msg.append(_('Planned vacation for: ') + str(date1))
                    else:
                        error.append(_('Already planned vacation for: ') + str(date1))
                else:
                    error.append(_('From must be before To'))

        if request.POST.get('action') == "delete":
            acID = int(request.POST.get('id_entry'))
            if acID > 0:
                Acquisition(user = request.user, id = acID).delete()

    vacation = UserProfile.objects.get(user = request.user).vacation_days
    vacation_used = len(allAcquisitions)

    if vacation_used == 0:
        percent = 0
    elif vacation_used > vacation:
        percent = 100
    else:
        percent = vacation_used*100/vacation

    c = {'user':request.user, 'SITENAME':settings.SITENAME, 'vacation_used':vacation_used, 'vacation':vacation, 'management':request.user.has_perm('auth.management'), 'percent':percent, 'form':form, 'today':today, 'acquisitions': allAcquisitions, 'msg':msg, 'error':error}
    c.update(csrf(request))
    return render_to_response('vacation.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def sick(request):
    logger.info('function_call sick(request) ->')

    msg = []
    error = []
    form = VacationForm()
    today = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
    allAcquisitions = Acquisition.objects.all().filter(user=request.user, project = Project.objects.get(name='Ill'))

    if request.method == 'POST':
        if request.POST.get('action') == "add":
            form = VacationForm(request.POST)

            if form.is_valid():
                date1 = form.cleaned_data['date1']
                date2 = form.cleaned_data['date2']
                if date1 < date2:
                    while date1 <= date2:
                        if form.cleaned_data['include_weekend'] == False:
                            if date1.isoweekday() == 6 or date1.isoweekday() == 7:
                                date1 = date1 + datetime.timedelta(days=1)
                                continue
                        if allAcquisitions.filter(start=date1):
                            error.append(_('Already planed for: ') + str(date1))
                            date1 = date1 + datetime.timedelta(days=1)
                            continue
                        acquisition = Acquisition(user = request.user, project = Project.objects.get(name = 'Ill'), comment = '', start = date1, end = date1 + datetime.timedelta(days=1))
                        acquisition.save()
                        date1 = date1 + datetime.timedelta(days=1)
                        msg.append(_('Planned for: ') + str(date1))

                elif date1 == date2:
                    if not allAcquisitions.filter(start=date1):
                        acquisition = Acquisition(user = request.user, project = Project.objects.get(name = 'Ill'), comment = '', start = date1, end = date1 + datetime.timedelta(days=1))
                        acquisition.save()
                        msg.append(_('Planned for: ') + str(date1))
                    else:
                        error.append(_('Already vacation for: ') + str(date1))
                else:
                    error.append(_('From must be before To'))

        if request.POST.get('action') == "delete":
            acID = int(request.POST.get('id_entry'))
            if acID > 0:
                Acquisition(user = request.user, id = acID).delete()

    vacation = UserProfile.objects.get(user = request.user).vacation_days
    vacation_used = len(allAcquisitions)

    if vacation_used == 0:
        percent = 0
    elif vacation_used > vacation:
        percent = 100
    else:
        percent = vacation_used*100/vacation

    c = {'user':request.user, 'SITENAME':settings.SITENAME, 'sick_used':vacation_used, 'sick':vacation, 'management':request.user.has_perm('auth.management'), 'percent':percent, 'form':form, 'today':today, 'acquisitions': allAcquisitions, 'msg':msg, 'error':error}
    c.update(csrf(request))
    return render_to_response('sick.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required('auth.management')
def analysis(request):
    logger.info('function_call analysis(request) ->')
    
    c = {'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('analysis.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required('auth.management')
def analysis_projects(request):
    logger.info('function_call analysis_projects(request) ->')
    
    projects = Project.objects.all().exclude(name = 'Vacation').exclude(name = 'Ill')
    
    for project in projects:
        project.consumed = project.consumed()
        project.hours = 0
        #project.budget = str(float("%.2f" % (project.budget/project.hourly_rate)))
        
        for member in Membership.objects.filter(project = project):
            project.hours = project.hours + member.hours

    c = {'user':request.user, 'projects': projects, 'SITENAME':settings.SITENAME, "currency":settings.CURRENCY, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('analysis_projects.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def analysis_project(request):
    logger.info('function_call analysis_project(request) ->')

    if request.method == 'POST':
        id = int(request.POST.get('id_project'))
        project = Project.objects.get(id = id)
        acquisitions = Acquisition.objects.all().filter(project=project)

    c = {'user':request.user, 'project': project, 'SITENAME':settings.SITENAME, "acquisitions":acquisitions, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('analysis_project.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required('auth.management')
def analysis_customers(request):
    logger.info('function_call analysis_customers(request) ->')
    
    customers = Customer.objects.all()
    
    for customer in customers:
        projects = []
        for project in customer.projects():
            project.consumed = project.consumed()
            project.hours = 0
            
            for member in Membership.objects.filter(project = project):
                project.hours = project.hours + member.hours

            projects.append(project)

        customer.projectlist = projects
    
    c = {'user':request.user, 'customers': customers, 'SITENAME':settings.SITENAME, "currency":settings.CURRENCY, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('analysis_customers.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def analysis_violations(request):
    logger.info('function_call analysis_violations(request) ->')

    if request.method == 'POST':
        logger.info('Executing Query().analysis_violation')
        for user in User.objects.all():
            Query().analysis_violation(user)

    violations = Violation.objects.all()
    
    c = {'user':request.user, 'violations': violations, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('analysis_violation.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def analysis_staff(request):
    logger.info('function_call analysis_staff(request) ->')

    userRequest = 0
    projects = []
    assigned = 0
    form = UserListForm()

    if request.method == 'POST':
        form = UserListForm(request.POST)

        if form.is_valid():
            userRequest = UserProfile.objects.get(user = form.cleaned_data['user'])
            form = UserListForm(initial={'user':userRequest})
            projects = Membership.objects.filter(user = userRequest.user)

            for project in projects:
                assigned = assigned + project.hours

    c = {'user':request.user, 'assigned': assigned, 'form':form, 'userRequest':userRequest, 'projects':projects, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('analysis_staff.html', c, context_instance=RequestContext(request))


def crons_violations(request):
    logger.info('function_call crons_violations(request) ->')

    for user in User.objects.all():
        Query().analysis_violation(user)

    c = {}
    c.update(csrf(request))
    return render_to_response('cron.html', c, context_instance=RequestContext(request))


@csrf_exempt
def password(request):
    logger.info('function_call password(request) ->')

    c = {'error': _('User not found'), 'SITENAME':settings.SITENAME}

    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            user = User.objects.all().filter(email = form.cleaned_data['email'])

            if len(user) == 1:
                pass_size = 6
                password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(pass_size))

                mail.mail_password_reset(user[0], password)

                user[0].set_password(password)
                user[0].save()

                c = {'msg': _('Password resetted'), 'SITENAME':settings.SITENAME}

            if len(user) > 1:
                c = {'error': _('User not identical. More then one user with this email'), 'SITENAME':settings.SITENAME}
                logger.critical('More then one User for one Email found: ' + form.cleaned_data['email'])

    c.update(csrf(request))
    return render_to_response('login.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def user_csv(request):
    logger.info('function_call user_csv(request) ->')

    msg = []
    error = []
    today = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
    form = DatePeriodForm()
    uploadForm = UploadFileForm()

    if request.method == 'POST':
        if request.POST.get('action') == "export":
            form = DatePeriodForm(request.POST)

            if form.is_valid():
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="export.csv"'

                start = form.cleaned_data['date1']
                end = form.cleaned_data['date2']

                writer = csv.writer(response)
                writer.writerow([_('Customer'), _('Project'), _('Location'), _('Comment'), _('Start'), _('End'), _('Billable')])
                for entry in Acquisition.objects.all().filter(user=request.user, end__lte=end+datetime.timedelta(days=1), start__gte=start).exclude(project = Project.objects.get(name='Vacation')).exclude(project = Project.objects.get(name='Ill')):
                    writer.writerow([entry.project.customer.name, entry.project.name, entry.location, entry.comment, entry.start, entry.end, entry.billable])

                return response

        if request.POST.get('action') == "import":
            uploadForm = UploadFileForm(request.POST, request.FILES)
            if uploadForm.is_valid():
                file = request.FILES['file']
                reader = csv.DictReader(file)

                for row in reader:
                    project = Project.objects.get(name = row[_('Project')])
                    location = Location.objects.get(name = row[_('Location')])
                    comment=row[_('Comment')]

                    if Membership.objects.all().filter(user=request.user, project=project) and not Acquisition.objects.all().filter(user = request.user, project = project, location = location, start = row[_('Start')], end = row[_('End')]):
                        if not comment:
                            acquisition = Acquisition(user = request.user, project = project, location = location, start = row[_('Start')], end = row[_('End')], billable = row[_('Billable')])
                        else:
                            acquisition = Acquisition(user = request.user, project = project, location = location, comment = comment, start = row[_('Start')], end = row[_('End')], billable = row[_('Billable')])
                        msg.append(_('Import: ') + str(row))
                        acquisition.save()
                    else:
                        logger.error('could not import csv entry for ' +str(request.user) + ': ' + str(row))
                        error.append(_('Could not import: ') + str(row))

    c = {'user':request.user, 'SITENAME':settings.SITENAME, 'form':form, 'formupload':uploadForm, 'today':today, 'management':request.user.has_perm('auth.management'), 'msg':msg, 'error':error}
    c.update(csrf(request))
    return render_to_response('user_csv.html', c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def project_csv(request):
    logger.info('function_call project_csv(request) ->')

    if request.method == 'POST':
        id = int(request.POST.get('id_project'))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)
        writer.writerow([_('Employe'), _('Date'), _('Start'), _('End'), _('Location'), _('Comment'), _('Duration in hours'), _('Billable')])
        for entry in Acquisition.objects.all().filter(project=Project.objects.get(id = id)):
            writer.writerow([entry.user.first_name + " " + entry.user.last_name, entry.start.date(), entry.start.time(), entry.end.time(), entry.location, entry.comment, entry.duration(), entry.billable])

        return response

    return HttpResponseRedirect(reverse('acquisition'))