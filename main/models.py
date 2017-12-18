from django.db.models import BooleanField, Model


class SiteSetting(Model):
    site_closed = BooleanField(default=True)