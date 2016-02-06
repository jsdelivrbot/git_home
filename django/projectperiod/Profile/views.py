# Create your views here.
# -*- coding: utf-8 -*- needed for regular expressions with äöü-characters


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import *
from django.conf import settings
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
import logging
import base64
import os

from Crypto.Cipher import AES
from Core.forms import *
from API.views_api import *
from Core.crypto import Crypto

logger = logging.getLogger(__name__)
crypto = Crypto()

@csrf_exempt
@login_required
def usersettings(request):
    logger.info('function_call usersettings(request) ->')

    usersettings = UserProfile.objects.get(user=request.user)
    form = UserSettingsForm(initial={'firstname':request.user.first_name, 'lastname':request.user.last_name, 'startday':usersettings.startday, 'endday':usersettings.endday, 'steps':usersettings.steps, 'acquisition':usersettings.acquisition, 'email':request.user.email})

    if request.method == 'POST':
        form = UserSettingsForm(request.POST)

        if form.is_valid():
            usersettings.startday = form.cleaned_data['startday']
            usersettings.endday = form.cleaned_data['endday']
            usersettings.steps = form.cleaned_data['steps']
            usersettings.acquisition = form.cleaned_data['acquisition']
            usersettings.save()

            user= User.objects.get(id=request.user.id)
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.email = form.cleaned_data['email']
            user.save()

    c = {'user':request.user, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('usersettings.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def changepassword(request):
    logger.info('function_call changepassword(request) ->')

    msg = []
    error = []
    form = ChangePasswordForm()
    user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            userAuth = authenticate(username=user, password=form.cleaned_data['old'])
            if form.cleaned_data['new1'] != form.cleaned_data['new2']:
                error.append(_('New password must be identical for both fields'))
            elif userAuth is None:
                error.append(_('Old password does not match'))
            else:
                user.set_password(form.cleaned_data['new2'])
                user.save()
                msg.append(_('Password changed'))

    c = {'user':request.user, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management'), 'msg':msg, 'error':error}
    c.update(csrf(request))
    return render_to_response('changepassword.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def integrations(request):
    logger.info('function_call integrations(request) ->')

    msg = []
    error = []

    integrations = Integration.objects.filter(user = request.user)

    if request.method == 'POST':
        if request.POST.get('action') == "delete":
            Integration.objects.get(id = int(request.POST.get('id_integration'))).delete()
            form = IntegrationForm()

        else:
            form = IntegrationForm(request.POST)

            if form.is_valid():
                password = crypto.encrypt(form.cleaned_data['password'])

                integration = Integration(user = request.user, tool = form.cleaned_data['tool'], project = form.cleaned_data['project'], url = form.cleaned_data['url'], username = form.cleaned_data['username'], password = password, query = form.cleaned_data['query'])
                integration.save()
                msg.append(_('New Integration appended'))
                form = IntegrationForm()
    else:
        form = IntegrationForm()

    c = {'user':request.user, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management'), 'msg':msg, 'error':error, 'integrations':integrations}
    c.update(csrf(request))
    return render_to_response('integrations.html', c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def integration(request):
    logger.info('function_call integration(request) ->')

    if request.method == 'POST':
        integration = Integration.objects.get(id = int(request.POST.get('id_integration')))

        form = IntegrationForm(instance=integration)

        if request.POST.get('action'):
            if request.POST.get('action') == "modifie":
                form = IntegrationForm(request.POST, instance=integration)
                if form.is_valid():
                    form.save()
                    integration.password = crypto.encrypt(form.cleaned_data['password'])
                    integration.save()
                    return HttpResponseRedirect(reverse('integrations'))

    c = {'user':request.user, 'integration':integration, 'form':form, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management')}
    c.update(csrf(request))
    return render_to_response('integration.html', c, context_instance=RequestContext(request))