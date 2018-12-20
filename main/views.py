from random import randint

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.views.generic import FormView
from django.views.generic import TemplateView

from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from registration.forms import User
from reportlab.graphics.barcode import code93
from reportlab.lib.units import cm, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from reportlab.pdfgen import canvas

from account.models import MassMedia, Reporter
from accr import settings
from accr.settings import ACCESS_COVER
from main.forms import ReporterForm
from main.models import SiteSetting

from .forms import ResendActivationEmailForm
from django.core import signing
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


class MainPageView(TemplateView):
    template_name = 'main_page.html'

    def dispatch(self, request, *args, **kwargs):
        site_settings = SiteSetting.objects.first()

        if site_settings.site_closed:
            self.template_name = 'site_closed.html'

        if request.user.is_authenticated():
            return HttpResponseRedirect('/account/')
        else:
            return super(MainPageView, self).dispatch(request)


class AccessCardView(SingleObjectMixin, FormView, ContextMixin):
    """ Application for accreditation, pdf document """
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="application.pdf"'

    response['Content-Disposition'] = 'filename="application.pdf"'
    success_url = '/card/'
    template_name = 'access_card_report.html'
    form_class = ReporterForm

    def report(self, reporters):
        # Create the PDF object, using the response object as its "file."
        pdf = canvas.Canvas(self.response)

        times_bold = ttfonts.TTFont('TimesBold', 'Times New Roman Cyr Bold.ttf')
        times = ttfonts.TTFont('Times', 'Times New Roman Cyr.ttf')
        pdfmetrics.registerFont(times_bold)
        pdfmetrics.registerFont(times)
        saved = False
        access_cover = ImageReader(ACCESS_COVER)
        times_bold = ttfonts.TTFont('TimesBold', 'Times New Roman Cyr Bold.ttf')
        times = ttfonts.TTFont('Times', 'Times New Roman Cyr.ttf')
        pdfmetrics.registerFont(times_bold)
        pdfmetrics.registerFont(times)

        count = 1

        margin = self.margins()

        for reporter in reporters:
            if count % 5 == 0:
                pdf.showPage()
                margin = self.margins()
                saved = True
            else:
                saved = False
            pdf.drawImage(access_cover, 3 * cm, margin['main_cover'] * cm, 13.75 * cm, 4.5 * cm)
            try:
                reporter_face = ImageReader(reporter.image_crop)
            except:
                reporter_face = ImageReader('main/static/main/img/unknown.jpg')
            pdf.drawImage(reporter_face, 3.2 * cm, margin['face'] * cm, 2.83 * cm, 3.7 * cm)
            watermark = ImageReader('access_watermark.png')
            pdf.drawImage(watermark, 3.02 * cm, margin['watermark'] * cm, 4.3 * cm, 4.45 * cm, mask='auto')

            pdf.setFont("TimesBold", 13)

            if len(reporter.surname) > 13:
                pdf.setFont("TimesBold", 11)
            pdf.drawString(6.3 * cm, margin['surname'] * cm, reporter.surname)
            pdf.drawString(6.3 * cm, margin['name'] * cm, reporter.name)
            pdf.drawString(6.3 * cm, margin['lastname'] * cm, reporter.lastname)

            pdf.setFont("TimesBold", 11)
            pdf.setFillColorRGB(255, 0, 0)
            if len(reporter.post) < 16:
                pdf.drawString(6.3 * cm, margin['post'] * cm, reporter.post)
            else:
                pdf.drawString(6.3 * cm, margin['post'] * cm, reporter.post[0:16])
                pdf.drawString(6.3 * cm, (margin['post'] - 0.42) * cm, reporter.post[16:32])

            pdf.setFillColorRGB(0, 0, 161)
            if len(reporter.massmedia.__str__()) < 16:
                pdf.drawString(6.3 * cm, margin['massmedia'] * cm, reporter.massmedia.__str__())
            else:
                pdf.drawString(6.3 * cm, margin['massmedia'] * cm, reporter.massmedia.__str__()[0:17])
                pdf.drawString(6.3 * cm, (margin['massmedia'] - 0.42) * cm, reporter.massmedia.__str__()[16:32])

            unique_num = randint(100001, 999999)
            unique_str = "PR-%s-%s" % (16, unique_num)

            pdf.setFont("TimesBold", 9)
            pdf.setFillColorRGB(255, 0, 0)
            pdf.drawString(3.6 * cm, margin['u_str_left'] * cm, unique_str)
            pdf.setFillColorRGB(0, 0, 161)
            pdf.drawString(14.35 * cm, margin['u_str_right'] * cm, unique_str)

            # qrw = QrCodeWidget('Helo World!')
            # qrw.draw()

            barcode = code93.Standard93(str(unique_num), barWidth=0.25 * mm, barHeight=15 * mm)

            # drawOn puts the barcode on the canvas at the specified coordinates

            pdf.setFillColorRGB(0, 0, 0)
            barcode.drawOn(pdf, 9.5 * cm, margin['barcode'] * cm)
            pdf.drawString(10.8 * cm, margin['barcode_num'] * cm, str(unique_num))

            for key, value in margin.items():
                margin[key] = value - 5

            reporter.printed = True
            reporter.save()
            count += 1

        if not saved:
            pdf.showPage()
        pdf.save()
        return self.response

    def get_context_data(self, **kwargs):
        massmedias = MassMedia.objects.all()
        reporters = []
        for mm in massmedias:
            for rep in mm.reporter_set.all():
                if rep.image_crop:
                    reporters.append(rep)
        reporters.sort(key=lambda rep: rep.updated, reverse=True)
        context = dict()
        context['reporters'] = reporters
        return context

    def post(self, request, *args, **kwargs):
        # print(self.request.POST)
        form = self.get_form()
        # print(form)
        if not form.is_valid():
            return HttpResponseRedirect('/card/')
        reporters = form.cleaned_data['reporter']

        # reporters = form.cleaned_data['reporter']
        # reporters = {}
        # for massmedia in massmedias:
        #     for reporter in massmedia.reporter_set.all():
        #         reporters[reporter.id] = reporter.__str__()
        # print(reporters)
        # for massmedia
        return self.report(reporters)

    def margins(self):
        margin = {
            'main_cover': 23.5,
            'face': 24.04,
            'surname': 27.4,
            'name': 26.8,
            'lastname': 26.2,
            'post': 25.5,
            'massmedia': 24.5,
            'u_str_left': 23.65,
            'u_str_right': 26.15,
            'barcode': 23.9,
            'barcode_num': 23.6,
            'watermark': 23.53,
        }
        return margin


class NewDesign(TemplateView):
    template_name = 'base_old.html'


# todo make CBV
def resend_activation_email(request):
    email_body_template = 'registration/activation_email.txt'
    email_subject_template = 'registration/activation_email_subject.txt'

    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')

    context = Context()

    form = None
    if request.method == 'POST':
        form = ResendActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email, is_active=0)

            if not users.count():
                form._errors["email"] = 'Учетная запись на таком e-mail не найдена или уже зарегистрирована.'

            REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT', 'registration')
            print(REGISTRATION_SALT)
            for user in users:
                activation_key = signing.dumps(
                    obj=getattr(user, user.USERNAME_FIELD),
                    salt=REGISTRATION_SALT,
                )
                context = {}
                context['activation_key'] = activation_key
                context['expiration_days'] = settings.ACCOUNT_ACTIVATION_DAYS
                context['site'] = get_current_site(request)

                subject = render_to_string(email_subject_template,
                                           context)
                # Force subject to a single line to avoid header-injection
                # issues.
                subject = ''.join(subject.splitlines())
                message = render_to_string(email_body_template,
                                           context)
                user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
                context['email'] = form.cleaned_data["email"]
                return render(request, 'registration/resend_activation_email_done.html', context)

    if not form:
        form = ResendActivationEmailForm()

    context.update({"form": form})
    return render(request, 'registration/resend_activation_email_form.html', context)
