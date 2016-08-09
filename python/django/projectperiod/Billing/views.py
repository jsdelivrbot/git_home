# Create your views here.
# -*- coding: utf-8 -*- needed for regular expressions with äöü-characters


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Permission, ContentType
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import *
from django.template import RequestContext
from django.utils.translation import ugettext as _
from reportlab.lib.validators import Auto
from Core.forms import *
from API.views_api import *
from Core.tables import *
from django_tables2   import RequestConfig
from Core.mail import Mail

import logging
import csv

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
@permission_required('auth.management')
def billing(request):
    logger.info('function_call billing(request) ->')

    if len(BillingIntegration.objects.all()) == 0:
        c = {'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
        c.update(csrf(request))
        return render_to_response('billing_empty.html', c, context_instance=RequestContext(request))

    form = BillingForm()

    if request.method == 'POST':
        form = BillingForm(request.POST)

        if form.is_valid():
            billing = Billing(project = form.cleaned_data['project'], tool = form.cleaned_data['tool'], start = form.cleaned_data['start'], end = form.cleaned_data['end'], type = form.cleaned_data['type'])
            if form.cleaned_data['tool'].tool == 0:
                return billing_csv(billing)
            elif form.cleaned_data['tool'].tool == 1:
                billing_mail(billing)

    c = {'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management'), 'form':form}
    c.update(csrf(request))
    return render_to_response('billing.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def auto_billings(request):
    logger.info('function_call auto_billings(request) ->')

    billings = Billing.objects.all()

    if request.method == 'POST':
        if request.POST.get('action') == "delete":
            billing = Billing.objects.get(id = int(request.POST.get('id_record')))
            billing.delete()

            form = BillingForm()

        else:
            form = BillingForm(request.POST)

            if form.is_valid():
                form.save()
                form = BillingForm()
    else:
        form = BillingForm()

    table = BillingTable(billings)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    c = {'table':table, 'form': form, 'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('auto_billings.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def auto_billing(request):
    logger.info('function_call auto_billing(request) ->')

    if request.method == 'POST':
        billing = Billing.objects.get(id = int(request.POST.get('id_record')))

        form = BillingForm(instance=billing)

        if request.POST.get('action'):
            if request.POST.get('action') == "modifie":
                form = BillingForm(request.POST, instance=billing)

                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('auto_billings'))

    c = {'user':request.user, 'billing':billing, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('auto_billing.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def billing_integrations(request):
    logger.info('function_call billing_integrations(request) ->')

    billings = BillingIntegration.objects.all()

    if request.method == 'POST':
        if request.POST.get('action') == "delete":
            billing = BillingIntegration.objects.get(id = int(request.POST.get('id_record')))
            billing.delete()

            form = BillingIntegrationForm()

        else:
            form = BillingIntegrationForm(request.POST)

            if form.is_valid():
                form.save()
                form = BillingIntegrationForm()
    else:
        form = BillingIntegrationForm()

    table = BillingIntegrationTable(billings)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    c = {'table':table, 'form': form, 'user':request.user, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('billing_integrations.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required('auth.management')
def billing_integration(request):
    logger.info('function_call billing_integration(request) ->')

    if request.method == 'POST':
        billing = BillingIntegration.objects.get(id = int(request.POST.get('id_record')))

        form = BillingIntegrationForm(instance=billing)

        if request.POST.get('action'):
            if request.POST.get('action') == "modifie":
                form = BillingIntegrationForm(request.POST, instance=billing)

                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('billing_integrations'))

    c = {'user':request.user, 'billing':billing, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('billing_integration.html', c, context_instance=RequestContext(request))


def crons_billings(request):
    logger.info('function_call crons_billings(request) ->')

    today = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)

    for billing in Billing.objects.filter(end__lte=today):
        if billing.tool.tool == 1: #EMail
            billing_mail(billing)
            billing.delete()

    c = {}
    c.update(csrf(request))
    return render_to_response('cron.html', c, context_instance=RequestContext(request))


def billing_mail(billing):
    acquisitions = Acquisition.objects.filter(project = billing.project)
    if billing.start:
        acquisitions = acquisitions.filter(start__gte=billing.start)
    if billing.end:
        acquisitions = acquisitions.filter(start__lte=billing.end + datetime.timedelta(days=1))
    budget = 0
    if billing.type == 1:
        budget = billing.project.budget
        acquisitions = []
    elif billing.type == 2:
        acquisitions = acquisitions.filter(billable=True)
    elif billing.type == 3:
        budget = billing.project.budget
        acquisitions = acquisitions.filter(billable=True)
    Mail().mail_bill(billing.tool.mail, acquisitions, budget, billing.project)


def billing_csv(billing):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    writer.writerow([_('Project'), _('Location'), _('Employe'), _('Comment'), _('Start'), _('End'), _('Cost')])
    if billing.type == 0:
        entries = Acquisition.objects.all().filter(project=billing.project)
    elif billing.type == 1:
        writer.writerow(['', billing.project, '', '', '', '', billing.project.budget])
        entries = []
    elif billing.type == 2:
        entries = Acquisition.objects.all().filter(project=billing.project, billable=True)
    elif billing.type == 3:
        writer.writerow(['', billing.project, '', '', '', '', billing.project.budget])
        entries = Acquisition.objects.all().filter(project=billing.project, billable=True)
    if billing.start:
        entries = entries.filter(start__gte=billing.start)
    if billing.end:
        entries = entries.filter(end__lte=billing.end + datetime.timedelta(days=1))
    for entry in entries:
        writer.writerow(
            [entry.project.name, entry.location, entry.user.last_name + ' ' + entry.user.first_name, entry.comment,
             entry.start, entry.end, entry.cost()])

    return response