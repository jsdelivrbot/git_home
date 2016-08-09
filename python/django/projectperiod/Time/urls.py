from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

from Core import views
from API import views_api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/customers', views.CustomerViewSet)
router.register(r'api/projects', views.ProjectViewSet)
router.register(r'api/acquisitions', views.AcquisitionViewSet)
router.register(r'api/locations', views.LocationViewSet)

urlpatterns = patterns('',

    url(r'^login/$', 'Auth.views.login_user', name="login"),
    url(r'^logout/$', 'Auth.views.logout_user', name="logout"),
    
    url(r'^$', 'Core.views.index_redirect', name='empty'),
    url(r'^acquisition/$', 'Core.views.acquisition', name="acquisition"),
    url(r'^acquisition_explicit/$', 'Core.views.acquisition_explicit', name="acquisition_explicit"),
    url(r'^acquisition_counter/$', 'Core.views.acquisition_counter', name="acquisition_counter"),
    url(r'^overview_day/$', 'Core.views.overview_day', name="overview_day"),
    url(r'^overview_week/$', 'Core.views.overview_week', name="overview_week"),
    url(r'^overview_month/$', 'Core.views.overview_month', name="overview_month"),
    url(r'^overview_year/$', 'Core.views.overview_year', name="overview_year"),
    url(r'^personal_budget/$', 'Core.views.personal_budget', name="personal_budget"),
    url(r'^analysis/$', 'Core.views.analysis', name="analysis"),
    url(r'^analysis_customers/$', 'Core.views.analysis_customers', name="analysis_customers"),
    url(r'^analysis_projects/$', 'Core.views.analysis_projects', name="analysis_projects"),
    url(r'^analysis_project/$', 'Core.views.analysis_project', name="analysis_project"),
    url(r'^analysis_violations/$', 'Core.views.analysis_violations', name="analysis_violations"),
    url(r'^analysis_staff/$', 'Core.views.analysis_staff', name="analysis_staff"),
    url(r'^password/$', 'Core.views.password', name="password"),
    url(r'^user_csv/$', 'Core.views.user_csv', name="user_csv"),
    url(r'^project_csv/$', 'Core.views.project_csv', name="project_csv"),
    url(r'^vacation/$', 'Core.views.vacation', name="vacation"),
    url(r'^sick/$', 'Core.views.sick', name="sick"),
    url(r'^crons/violations/$', 'Core.views.crons_violations', name="crons_violations"),

    url(r'^staff/$', 'Planning.views.staff', name="staff"),
    url(r'^employe/$', 'Planning.views.employe', name="employe"),
    url(r'^locations/$', 'Planning.views.locations', name="locations"),
    url(r'^location/$', 'Planning.views.location', name="location"),
    url(r'^customers/$', 'Planning.views.customers', name="customers"),
    url(r'^customer/$', 'Planning.views.customer', name="customer"),
    url(r'^projects/$', 'Planning.views.projects', name="projects"),
    url(r'^project/$', 'Planning.views.project', name="project"),
    url(r'^management/$', 'Planning.views.management', name="management"),

    url(r'^billing/$', 'Billing.views.billing', name="billing"),
    url(r'^auto_billings/$', 'Billing.views.auto_billings', name="auto_billings"),
    url(r'^auto_billing/$', 'Billing.views.auto_billing', name="auto_billing"),
    url(r'^billings_integration/$', 'Billing.views.billing_integrations', name="billing_integrations"),
    url(r'^billing_integration/$', 'Billing.views.billing_integration', name="billing_integration"),
    url(r'^crons/billings/$', 'Billing.views.crons_billings', name="crons_billings"),

    url(r'^usersettings/$', 'Profile.views.usersettings', name="usersettings"),
    url(r'^changepassword/$', 'Profile.views.changepassword', name="changepassword"),
    url(r'^integrations/$', 'Profile.views.integrations', name="integrations"),
    url(r'^integration/$', 'Profile.views.integration', name="integration"),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^api_getWorkItems/$', 'API.views.api_getWorkItems', name="api_getWorkItems"),

    url(r'^', include(router.urls)),
)