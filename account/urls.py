from django.conf import settings
from django.conf.urls import include, url

# from .views import (
#     news_list
# )
from django.contrib.auth.decorators import login_required
from registration.views import RegistrationView

# from main.forms import UserForm
from account import views
from .views import (
    MassMediaView, MassMediaCreate, MassMediaUpdate, ReporterCreate, ReporterUpdate, ReporterDelete, ImageCrop,
    ReportAccount)

urlpatterns = [
    url(r'^$', login_required(MassMediaView.as_view()), name='profile'),
    # url(r'^edit/$', views.get_name, name='edit_massmedia'),
    url(r'^add/$', login_required(MassMediaCreate.as_view()), name='massmedia_create'),
    url(r'^(?P<pk>[0-9]+)/$', login_required(MassMediaUpdate.as_view()), name='massmedia_update'),
    url(r'^reporter/$', login_required(ReporterCreate.as_view()), name='reporter_create'),
    url(r'^reporter/(?P<pk>[0-9]+)/$', login_required(ReporterUpdate.as_view()), name='reporter_update'),
    url(r'^reporter/crop/(?P<pk>[0-9]+)/$', login_required(ImageCrop.as_view()), name='reporter_image'),
    # url(r'^reporter/image/$', ImageCrop.as_view(), name='reporter_image'),
    url(r'^reporter/delete/(?P<pk>[0-9]+)/$', login_required(ReporterDelete.as_view()), name='reporter_delete'),
    url(r'^report/(?P<pk>[0-9]+)/$', login_required(ReportAccount.as_view()), name='account_report'),
    # url(r'^accounts/', FormView.as_view(), name='form_test'),
]
