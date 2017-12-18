from django.db.models import BooleanField, Model


class SiteSettings(Model):
    site_closed = BooleanField(default=True)