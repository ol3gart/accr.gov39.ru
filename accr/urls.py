"""accr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_done
from django.views.generic import RedirectView
from registration.backends.hmac.views import RegistrationView

from accr import settings
from main.forms import RegistrationFormTOSAndEmail
from registration.forms import RegistrationFormUniqueEmail

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^', include('main.urls', namespace='main')),

                  url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormTOSAndEmail),
                      name='registration_register'),
                  url(r'^accounts/', include('registration.backends.hmac.urls')),

                  url(r'^accounts/profile/$', RedirectView.as_view(url='/account/', permanent=False),
                      name='ProfilePage'),
                  # url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/successfully_logged_out/'}),
                  url(r'account/', include('account.urls', namespace='account')),

                  # url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
                  # url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                  #     'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': '/user/password/done/'}),
                  # url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
