from django import forms

from .models import MassMedia, Reporter


# class MassMediaForm(forms.ModelForm):
#     class Meta:
#         model = MassMedia
#         fields = ['title', 'type', 'founder', 'statutory_task', 'address', 'phone']


# class ImageCropForm(forms.ModelForm):
#     class Meta:
#         model = Reporter
#         fields = ['']

class ImageCropForm(forms.Form):
    x = forms.DecimalField(label='x', max_digits=4, decimal_places=0)
    y = forms.DecimalField(label='y', max_digits=4, decimal_places=0)
    width = forms.DecimalField(label='width', max_digits=4, decimal_places=0)
    height = forms.DecimalField(label='height', max_digits=4, decimal_places=0)
