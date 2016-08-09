from Core.models import *

import django_tables2 as tables

ACTIONS_LOCATION = '''                           <span class="glyphicon glyphicon-pencil" style="font-size:20px;" onclick="edit_{{ record.pk }}.submit();"></span>
                                        {% if record.status == 0 %}<span class="glyphicon glyphicon-ok" style="font-size:20px;" onclick="delete_{{ record.pk }}.submit();"></span>{% else %}
                                        <span class="glyphicon glyphicon-remove" style="font-size:20px;" onclick="activate_{{ record.pk }}.submit();"></span>{% endif %}
                                        <form name="edit_{{ record.id }}" action="{% url "location" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                        </form>
                                        <form name="delete_{{ record.id }}" action="{% url "locations" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                            <input type="hidden" name="action" id="action" value="delete"/>
                                        </form>
                                        <form name="activate_{{ record.id }}" action="{% url "locations" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                            <input type="hidden" name="action" id="action" value="activate"/>
                                        </form>
'''

FLAGS = '''                             <img src="{{ record.country.flag }}" alt="{{ record.country.name }}" style="padding: 0px 10px 0px 0px"/>
'''


class LocationTable(tables.Table):
    class Meta:
        model = Location
        attrs = {"class": "table table-striped"}
        exclude = ("status", "id")
    Action = tables.TemplateColumn(ACTIONS_LOCATION, orderable=False)
    country = tables.TemplateColumn(FLAGS)


ACTIONS_CUSTOMER = '''                 <span class="glyphicon glyphicon-pencil" style="font-size:20px;" onclick="edit_{{ record.pk }}.submit();"></span>
                                        {% if record.status == 0 %}<span class="glyphicon glyphicon-ok" style="font-size:20px;" onclick="delete_{{ record.pk }}.submit();"></span>{% else %}
                                        <span class="glyphicon glyphicon-remove" style="font-size:20px;" onclick="activate_{{ record.pk }}.submit();"></span>{% endif %}
                                        <form name="edit_{{ record.id }}" action="{% url "customer" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                        </form>
                                        <form name="delete_{{ record.id }}" action="{% url "customers" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                            <input type="hidden" name="action" id="action" value="delete"/>
                                        </form>
                                        <form name="activate_{{ record.id }}" action="{% url "customers" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                            <input type="hidden" name="action" id="action" value="activate"/>
                                        </form>
'''


class CustomerTable(tables.Table):
    class Meta:
        model = Customer
        attrs = {"class": "table table-striped"}
        exclude = ("status", "id")
    Action = tables.TemplateColumn(ACTIONS_CUSTOMER, orderable=False)
    country = tables.TemplateColumn(FLAGS)


ACTIONS_STAFF = '''                     <span class="glyphicon glyphicon-pencil" style="font-size:20px;" onclick="edit_{{ record.id }}.submit();"></span>
                                        {% if record.is_active %}<span class="glyphicon glyphicon-ok" style="font-size:20px;" onclick="delete_{{ user.id }}.submit();"></span>{% else %}
                                        <span class="glyphicon glyphicon-remove" style="font-size:20px;" onclick="activate_{{ record.id }}.submit();"></span>{% endif %}
                                        <form name="edit_{{ record.id }}" action="{% url "employe" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                        </form>
                                        <form name="delete_{{ record.id }}" action="{% url "staff" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                            <input type="hidden" name="action" id="action" value="delete"/>
                                        </form>
                                        <form name="activate_{{ record.id }}" action="{% url "staff" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                            <input type="hidden" name="action" id="action" value="activate"/>
                                        </form>
'''


class StaffTable(tables.Table):
    class Meta:
        model = User
        attrs = {"class": "table table-striped"}
        exclude = ("id", "password", "last_login", "is_superuser", "is_staff", "is_active", "date_joined")
    Action = tables.TemplateColumn(ACTIONS_STAFF, orderable=False)


ACTIONS_PROJECTS = '''                  <span class="glyphicon glyphicon-pencil" style="font-size:20px;" onclick="edit_{{ record.id }}.submit();"></span>
'''


class ProjectTable(tables.Table):
    class Meta:
        model = Project
        attrs = {"class": "table table-striped"}
        exclude = ("id", "description", "budget", "billing", "hourly_rate")
    Action = tables.TemplateColumn(ACTIONS_PROJECTS, orderable=False)


ACTIONS_BILLINGS = '''                  <span class="glyphicon glyphicon-pencil" style="font-size:20px;" onclick="edit_{{ record.id }}.submit();"></span>
                                        <span class="glyphicon glyphicon-remove" style="font-size:20px;" onclick="delete_{{ record.id }}.submit();"></span>
                                        <form name="edit_{{ record.id }}" action="{% url "auto_billing" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                        </form>
                                        <form name="delete_{{ record.id }}" action="{% url "auto_billings" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                            <input type="hidden" name="action" id="action" value="delete"/>
                                        </form>
'''


class BillingTable(tables.Table):
    class Meta:
        model = Billing
        attrs = {"class": "table table-striped"}
        exclude = ("id")
    Action = tables.TemplateColumn(ACTIONS_BILLINGS, orderable=False)


ACTIONS_BILLINGINTEGRATIONS = '''                  <span class="glyphicon glyphicon-pencil" style="font-size:20px;" onclick="edit_{{ record.id }}.submit();"></span>
                                        <span class="glyphicon glyphicon-remove" style="font-size:20px;" onclick="delete_{{ record.id }}.submit();"></span>
                                        <form name="edit_{{ record.id }}" action="{% url "billing_integration" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                        </form>
                                        <form name="delete_{{ record.id }}" action="{% url "billing_integrations" %}" method="post">{% csrf_token %}
                                            <input type="hidden" name="id_record" id="id_record" value="{{ record.id }}"/>
                                            <input type="hidden" name="action" id="action" value="delete"/>
                                        </form>
'''


class BillingIntegrationTable(tables.Table):
    class Meta:
        model = BillingIntegration
        attrs = {"class": "table table-striped"}
        exclude = ("id", "password")
    Action = tables.TemplateColumn(ACTIONS_BILLINGINTEGRATIONS, orderable=False)