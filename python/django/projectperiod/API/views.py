# Create your views here.
# -*- coding: utf-8 -*- needed for regular expressions with äöü-characters

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.contrib.auth.decorators import *
from API.views_api import *
from API.TheBugGenie import TheBugGenie
from API.Polarion import Polarion
from Core.crypto import Crypto

import logging

logger = logging.getLogger(__name__)
crypto = Crypto()

@login_required
def api_getWorkItems(request):
    logger.info('function_call api_getWorkItems(request) ->')

    project = Project.objects.get(id = int(request.GET.get('id_project')))
    integrations = Integration.objects.all().filter(user = request.user, project = project)

    response = '{\n'

    if len(integrations) > 0:
        for integration in integrations:
            if integration.tool == 0:
                theBugGenie = TheBugGenie(integration.url, integration.username, integration.password)
                if theBugGenie.connected == True:
                    json = theBugGenie.getIssues()[0]['issues']
                    for issue in json:
                        response = response + '  "' + issue + '": "' + str(json[issue]['title']) + '",\n'
                else:
                    response = response + '  "' + 'Error' + '": "' + _('WorkItems could not be read') + '",\n'
            if integration.tool == 1:
                polarion = Polarion(integration.url, integration.username, crypto.decrypt(integration.password), integration.query)
                if polarion.connected == True:
                    workItems = polarion.getIssues()
                    for workitem in workItems:
                        response = response + '  "' + workitem.id + '": "' + workitem.title + '",\n'
                else:
                    response = response + '  "' + 'Error' + '": "' + _('WorkItems could not be read') + '",\n'

        if response == '{\n':
            response = response + '  "' + 'Info' + '": "' + _('No WorkItems found') + '"\n}'
        else:
            response = response[:-2] + '\n}'
    else:
        response = response + '  "' + 'Info' + '": "' + _('No Integration found') + '"\n}'

    return HttpResponse(response, content_type="application/json")