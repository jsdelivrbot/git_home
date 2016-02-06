from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
from Core.models import *
from django.conf import settings
from django.utils.translation import ugettext as _
from django.template.loader import get_template
from django.template import Context

import logging

logger = logging.getLogger(__name__)

recipient = []

class Mail(object):

    def mail_password_new(self, user, password):
        logger.info('mail send to created user ' + user.username)

        subject = "New Account for " + settings.SITENAME
        plaintext = get_template('email/password_new.txt')
        html = get_template('email/password_new.html')

        d = Context({ 'sitename': settings.SITENAME, 'url': settings.SITEURL, 'username': user.username, 'password':password })

        text_content = plaintext.render(d)
        html_content = html.render(d)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse( "Email sent" )
    
    def mail_password_reset(self, user, password):
        logger.info('mail send for password reset to user ' + user.username)

        subject = "New Password for " + settings.SITENAME
        plaintext = get_template('email/password_reset.txt')
        html = get_template('email/password_reset.html')

        d = Context({ 'sitename': settings.SITENAME, 'url': settings.SITEURL, 'username': user.username, 'password':password })

        text_content = plaintext.render(d)
        html_content = html.render(d)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse( "Email sent" )

    def mail_violation(self, user, violation):
        logger.info('mail send for violation to user ' + user.username)

        subject = 'Violation found on ' + settings.SITENAME
        plaintext = get_template('email/violation.txt')
        html = get_template('email/violation.html')

        d = Context({ 'violation': violation })

        text_content = plaintext.render(d)
        html_content = html.render(d)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse( "Email sent" )

    def mail_bill(self, email, acquisitions, budget, project):
        logger.info('mail send for billing ' + project.name)

        subject = "New Bill from " + settings.SITENAME
        plaintext = get_template('email/bill.txt')
        html = get_template('email/bill.html')

        d = Context({ 'budget': budget, 'acquisitions': acquisitions, 'currency': settings.CURRENCY, 'project':project })

        text_content = plaintext.render(d)
        html_content = html.render(d)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse( "Email sent" )
