from io import BytesIO
from io import StringIO

import os

import sys
from PIL import Image
from io import StringIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from pip._vendor.appdirs import unicode
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from account.forms import ImageCropForm
from account.models import MassMedia, Reporter


class MassMediaView(TemplateView):
    template_name = 'account/massmedia_view.html'

    # model = MassMedia

    def get_context_data(self, **kwargs):
        context = super(MassMediaView, self).get_context_data()
        massmedia = MassMedia.objects.filter(user=self.request.user).first()
        context['massmedia'] = massmedia
        # print(massmedia.reporter_count())
        # print(self.request.user)
        return context


class MassMediaCreate(CreateView):
    model = MassMedia
    fields = ['title', 'type', 'founder', 'statutory_task', 'address', 'phone']
    success_url = '/account/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MassMediaCreate, self).form_valid(form)


class MassMediaUpdate(UpdateView):
    model = MassMedia
    fields = ['title', 'type', 'founder', 'statutory_task', 'address', 'phone']
    success_url = '/account/'

    def get(self, *args, **kwargs):
        """ method for get only self massmedia model"""
        model_pk = kwargs.get('pk')
        massmedia = MassMedia.objects.filter(pk=model_pk).first()
        if massmedia and massmedia.user == self.request.user:
            return super(MassMediaUpdate, self).get(*args, **kwargs)
        else:
            return HttpResponseRedirect('/account/')

    def form_valid(self, form):
        """ method for update only self massmedia model"""
        if form.instance.user == self.request.user:
            return super(MassMediaUpdate, self).form_valid(form)
        else:
            return HttpResponseRedirect('/account/')


class ReporterCreate(CreateView):
    """ create reporter for massmedia account"""
    model = Reporter
    fields = ['surname', 'name', 'lastname', 'post', 'image']

    # success_url = '/account/reporter/crop/' + str(23)

    def get(self, request, *args, **kwargs):
        massmedia = MassMedia.objects.all().filter(user=self.request.user).first()
        if massmedia.reporter_count() >= massmedia.get_count():
            raise Http404
        return super(ReporterCreate, self).get(request)

    def get_success_url(self):
        reporter = Reporter.objects.all().filter(massmedia__user=self.request.user).order_by('-id').first()
        return '/account/reporter/crop/' + str(reporter.id)

    def form_valid(self, form):
        massmedia = MassMedia.objects.filter(user=self.request.user).first()
        form.instance.massmedia = massmedia
        return super(ReporterCreate, self).form_valid(form)


class ReporterUpdate(UpdateView):
    """ update reporter for massmedia account"""
    model = Reporter
    fields = ['surname', 'name', 'lastname', 'post', 'image']
    success_url = '/account/'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user"""
        obj = super(ReporterUpdate, self).get_object()
        massmedia = MassMedia.objects.all().filter(user=self.request.user).first()
        if not obj in massmedia.reporter_set.all():
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.printed = False
        obj.save()
        return super().post(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     massmedia = MassMedia.objects.get(user=self.request.user)
    #     reporter = Reporter.objects.filter(pk=kwargs['pk']).first()
    #     if reporter in massmedia.reporter_set.all().filter(massmedia=massmedia):
    #         return super(ReporterUpdate, self).get(request)
    #     else:
    #         return HttpResponseRedirect('/account/')

    def get_success_url(self):
        if self.request.FILES:
            return '/account/reporter/crop/' + str(self.kwargs['pk'])
        else:
            return '/account/'


class ImageCrop(DetailView):
    template_name = 'account/image_crop.html'
    model = Reporter

    def get_context_data(self, **kwargs):
        context = super(ImageCrop, self).get_context_data()
        # print(kwargs)
        return context

    def get(self, request, *args, **kwargs):
        massmedia = MassMedia.objects.get(user=self.request.user)
        reporter = Reporter.objects.filter(pk=kwargs['pk']).first()
        if reporter in massmedia.reporter_set.all().filter(massmedia=massmedia):
            return super(ImageCrop, self).get(request)
        else:
            return HttpResponseRedirect('/account/')

    def post(self, *args, **kwargs):
        form = ImageCropForm(self.request.POST)
        # print(form)
        if form.is_valid():
            reporter_id = kwargs['pk']
            reporter = Reporter.objects.get(id=reporter_id)

            image = Image.open(reporter.image)
            left = form.cleaned_data['x']
            top = form.cleaned_data['y']
            right = abs(form.cleaned_data['width'] + left)
            bottom = abs(form.cleaned_data['height'] + top)
            crop_image = image.crop((left, top, right, bottom))

            # print(crop_image)
            crop_image_io = BytesIO()
            crop_image.save(crop_image_io, format='JPEG')
            crop_image_file = InMemoryUploadedFile(crop_image_io, None, 'foo.jpg', 'image/jpeg',
                                                   sys.getsizeof(crop_image_io), None)

            reporter.image_crop = crop_image_file
            reporter.printed = False
            reporter.save()

            return HttpResponseRedirect('/account/')
        else:
            return HttpResponseRedirect('/account/reporter/crop/23/')


class ReporterDelete(DeleteView):
    """ delete reporter from massmedia account"""
    model = Reporter
    success_url = '/account/'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user"""
        obj = super(ReporterDelete, self).get_object()
        massmedia = MassMedia.objects.all().filter(user=self.request.user).first()
        if not obj.massmedia == massmedia:
            raise Http404
        return obj

    def get(self, *args, **kwargs):
        return HttpResponseRedirect('/account/')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        reporter = self.get_object()
        success_url = self.success_url
        reporter.status = False
        reporter.save()
        return HttpResponseRedirect(success_url)


class ReportAccount(TemplateView):
    """ Application for accreditation, pdf document """
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="application.pdf"'
    response['Content-Disposition'] = 'filename="application.pdf"'

    def report(self, *args, **kwargs):
        # Create the PDF object, using the response object as its "file."
        pdf = canvas.Canvas(self.response)
        times_bold = ttfonts.TTFont('TimesBold', 'Times New Roman Cyr Bold.ttf')
        times = ttfonts.TTFont('Times', 'Times New Roman Cyr.ttf')
        pdfmetrics.registerFont(times_bold)
        pdfmetrics.registerFont(times)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        massmedia = MassMedia.objects.get(user=self.request.user)

        for reporter in massmedia.reporter_set.all():
            print(reporter)
            reporter.printed = False
            reporter.save()
            pdf.setFont("TimesBold", 16)
            pdf.drawString(3 * cm, 27 * cm, "УЧЕТНАЯ КАРТОЧКА КОРРЕСПОНДЕНТА")
            pdf.setFont("Times", 15)

            if reporter.image_crop:
                image = ImageReader(reporter.image_crop)
            else:
                image = ImageReader('main/static/main/img/unknown.jpg')
            pdf.drawImage(image, 17 * cm, 23.5 * cm, 3 * cm, 4 * cm)

            pdf.drawString(3 * cm, 21 * cm, "Полное наименование СМИ:")
            pdf.setFont("TimesBold", 16)
            pdf.drawString(11 * cm, 21 * cm, massmedia.__str__())

            pdf.setFont("Times", 15)
            pdf.drawString(7.6 * cm, 20 * cm, "Фамилия:")
            pdf.setFont("TimesBold", 16)
            pdf.drawString(11 * cm, 20 * cm, reporter.surname)

            pdf.setFont("Times", 15)
            pdf.drawString(8.75 * cm, 19 * cm, "Имя:")
            pdf.setFont("TimesBold", 16)
            pdf.drawString(11 * cm, 19 * cm, reporter.name)

            pdf.setFont("Times", 15)
            pdf.drawString(7.6 * cm, 18 * cm, "Отчество:")
            pdf.setFont("TimesBold", 16)
            pdf.drawString(11 * cm, 18 * cm, reporter.lastname)

            pdf.setFont("Times", 15)
            pdf.drawString(4.2 * cm, 17 * cm, "Занимаемая должность:")
            pdf.setFont("TimesBold", 16)
            pdf.drawString(11 * cm, 17 * cm, reporter.post)

            pdf.setFont("Times", 13)
            pdf.drawString(4 * cm, 14 * cm, "Я,")
            pdf.setFont("TimesBold", 16)
            pdf.drawString(6 * cm, 14 * cm, reporter.__str__())
            pdf.line(4.8 * cm, 13.8 * cm, 18.5 * cm, 13.8 * cm)

            pdf.setFont("Times", 13)
            pdf.drawString(3 * cm, 13 * cm, "даю свое согласие на обработку моих персональных данных, предусмотренное")
            pdf.drawString(3 * cm, 12 * cm, "Законом Российской Федерации от 27.07.2006 № 152-ФЗ «О персональных")
            pdf.drawString(3 * cm, 11 * cm, "данных».")

            pdf.setFont("Times", 9)

            pdf.drawString(10.3 * cm, 8 * cm, "подпись")
            pdf.line(9 * cm, 8.5 * cm, 13 * cm, 8.5 * cm)
            pdf.drawString(14.2 * cm, 8 * cm, "расшифровка подписи")
            pdf.line(13.2 * cm, 8.5 * cm, 18.5 * cm, 8.5 * cm)
            pdf.drawString(13.7 * cm, 8.7 * cm,
                           "%s.%s. %s" % (reporter.name[0].upper(), reporter.lastname[0].upper(), reporter.surname))
            # pdf.drawString(10 * cm, 7 * cm, "М.П.")

            pdf.drawString(4.7 * cm, 5 * cm, "должность")
            pdf.line(3 * cm, 5.5 * cm, 8 * cm, 5.5 * cm)
            pdf.drawString(10.3 * cm, 5 * cm, "подпись")
            pdf.line(9 * cm, 5.5 * cm, 13 * cm, 5.5 * cm)
            pdf.drawString(14.2 * cm, 5 * cm, "расшифровка подписи")
            pdf.line(13.2 * cm, 5.5 * cm, 18.5 * cm, 5.5 * cm)
            pdf.drawString(10 * cm, 4 * cm, "М.П.")

            pdf.drawString(3 * cm, 2 * cm, 'Дата "____" _______________ 20_____ г.')

            pdf.showPage()
        # style = ParagraphStyle(name='test')
        # text = Paragraph("предусмотренное Законом Российской Федерации от 27 июля 2006 года № 152-ФЗ «О персональных данных».", style)
        # pdf.drawString(text)


        # Close the PDF object cleanly, and we're done.

        pdf.save()
        return self.response

    def dispatch(self, request, *args, **kwargs):
        if not self.is_valid():
            return HttpResponseRedirect('/account/')
        return super(ReportAccount, self).dispatch(request)

    @never_cache
    def get(self, *args, **kwargs):
        return self.report()

        @never_cache
    def post(self, *args, **kwargs):
        return self.report()

    def is_valid(self):
        massmedia = MassMedia.objects.filter(user=self.request.user).first()
        if massmedia and massmedia.reporter_count():
            return True
        return False
