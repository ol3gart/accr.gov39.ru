from django.contrib import admin

# Register your models here.
from account.models import MassMediaType, MassMedia, Reporter


class ReporterAdmin(admin.ModelAdmin):
    # fields = ('reporter', 'massmedia', 'post', 'status')
    # fields = ('reporter', 'status')
    list_display = ('id', 'surname', 'name', 'lastname', 'post', 'massmedia', 'image_crop', 'added', 'updated', 'status', 'printed')

    def get_queryset(self, request):
        return self.model._base_manager.get_queryset()


admin.site.register(MassMediaType)
admin.site.register(MassMedia)
admin.site.register(Reporter, ReporterAdmin)
