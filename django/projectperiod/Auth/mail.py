from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from Core.models import *
from django.conf import settings
from django.utils.translation import ugettext as _

import logging

logger = logging.getLogger(__name__)

recipient = []

class Mail(object):
    def mail_test(self, request, content, to):
        return HttpResponse( "Email sent" )
    
    def mail_password_new(self, user, password):
        logger.info('mail send to created user ' + user.username)

        message = "Dear user,\n\nyour account for " + settings.SITENAME + " has been created. Find below your credentials." + \
                    "\n\nUsername: " + user.username + \
                    "\nPassword: " + password + \
                    "\n\nYou can log in by using this url: \n" + settings.SITEURL

        recipient.append(user.email)
        send_mail('New Account for ' +settings.SITENAME, message, settings.EMAIL_FROM, recipient, fail_silently=False)
        return HttpResponse( "Email sent" )
    
    def mail_password_reset(self, user, password):
        logger.info('mail send for password reset to user ' + user.username)

        message = _("Dear user,\n\nyour password for ") + settings.SITENAME + _(" has been resetted. Find below your credentials.") + \
                    _("\n\nUsername: ") + user.username + \
                    _("\nPassword: ") + password + \
                    _("\n\nYou can log in by using this url: \n") + settings.SITEURL

        recipient.append(user.email)
        send_mail(_('New Password for ') + settings.SITENAME, message, settings.EMAIL_FROM, recipient, fail_silently=False)
        return HttpResponse( "Email sent" )