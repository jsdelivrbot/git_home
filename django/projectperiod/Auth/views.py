# Create your views here.
# -*- coding: utf-8 -*- needed for regular expressions with äöü-characters


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django_countries.fields import Country
import logging

from Core.mail import Mail
from API.views_api import *


logger = logging.getLogger(__name__)
mail = Mail()

@csrf_exempt
def login_user(request):
    logger.info('function_call login_user(request) ->')

    message = ""
    username = password = ''
    msg = ""
    error = ""
    MYLANGUAGES = []
    MYLANGUAGES.append(Country("DE"))
    MYLANGUAGES.append(Country("GB"))

    if settings.SERVICE == False:
        if request.user.is_anonymous():
            if request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
    
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        logger.debug("User Authentication: [%s] successfully logged in" % username)
                        if len(UserProfile.objects.all().filter(user=user)) == 0:
                            profile = UserProfile(user = user, startday = settings.USER_STARTDAY, endday = settings.USER_ENDDAY, steps = settings.USER_STEPS, min_hours = settings.USER_MIN_HOUR, max_hours = settings.USER_MAX_HOUR,
                                                  hourly_rate = settings.USER_HOURLY_RATE, vacation_days = settings.USER_VACATION_DAYS, acquisition = settings.USER_ACQUISITION)
                            profile.save()
                        if len(Customer.objects.all().filter(name='Intern')) == 0:
                            customer = Customer(name = 'Intern', street = '-', postcode = '-', city = '-', status = 0)
                            customer.save()
                        if len(Project.objects.all().filter(name='Vacation')) == 0:
                            project = Project(name = 'Vacation', description = 'Vacation', responsible = user, budget = 0, billing = 0, hourly_rate = 0, status = 0, customer = Customer.objects.get(name='Intern'))
                            project.save()
                        if len(Project.objects.all().filter(name='Ill')) == 0:
                            project = Project(name = 'Ill', description = 'Ill', responsible = user, budget = 0, billing = 0, hourly_rate = 0, status = 0, customer = Customer.objects.get(name='Intern'))
                            project.save()
                        return HttpResponseRedirect(reverse('acquisition'))
    
                    else:
                        error = _("Deactivated Account")
                        logger.debug("User Authentication: [%s] account inactive" % username)
                else:
                    error = _("Incorrect Login")
                    logger.debug("User Authentication: [%s] username and/or password incorrect" % username)
        else:
            logger.debug("User Authentication: [%s] already logged in" % username)
            return HttpResponseRedirect(reverse('acquisition'))
    else:
        if request.user.is_anonymous():
            if request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
        
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_superuser:
                        login(request, user)
                        return HttpResponseRedirect(reverse('acquisition'))
          
            error = _("Site is under maintenance")
            message = "error"

    c = {'msg':msg, 'error':error, 'user':request.user, 'message':message, 'SITENAME':settings.SITENAME, 'management':request.user.has_perm('auth.management'), 'SSL':settings.SSL_ENABLED, 'request':request, 'languages':MYLANGUAGES}
    c.update(csrf(request))
    return render_to_response('login.html', c, context_instance=RequestContext(request))


@csrf_protect
def logout_user(request):
    logger.info('function_call logout_user(request) ->')

    if request.user.is_authenticated():
        username = request.user.username
        logout(request)
        logger.debug("User Authentication: [%s] successfully logged out" % username)

    return HttpResponseRedirect(reverse('acquisition'))