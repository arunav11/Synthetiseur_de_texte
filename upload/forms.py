from django import forms
from django.utils.translation import ugettext_lazy as _

from upload.models import MediaFile


class MediaFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MediaFileForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['file'].widget.attrs['accept'] = ".wav,.mp4"
        self.fields['file'].widget.attrs['class'] = 'form-control-file'
        self.fields['file'].widget.attrs['style'] = 'text-align: center; width: fit-content; display: -webkit-inline-box;'
        self.fields['file'].widget.attrs['id'] = 'file'

    class Meta:
        model = MediaFile
        fields = ['file']
        labels = {
            'file': _('')
        }
        error_messages = {
            'file': {
                'required': _('Please choose the file')
            }
        }

