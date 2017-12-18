from django.conf import settings
from django.conf.urls import include, url

# from .views import (
#     news_list
# )
from registration.views import RegistrationView

# from main.forms import UserForm
from main.views import resend_activation_email
from .views import (
    MainPageView,
    AccessCardView, NewDesign)

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main_page'),
    url(r'^card/$', AccessCardView.as_view(), name='access_card'),
    url(r'^new/$', NewDesign.as_view(), name='new_design'),
    url(r'^accounts/reactivate/$', resend_activation_email, name='account_reactivate'),
]
