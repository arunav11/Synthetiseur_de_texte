from django import forms
from django.utils.translation import ugettext_lazy as _

from upload.models import MediaFile


class MediaFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MediaFileForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['photo'].widget.attrs['accept'] = ".wav,.mp4"

    class Meta:
        model = MediaFile
        fields = '__all__'
        labels = {
            'photo': _('Choose Media File')
        }
        error_messages = {
            'photo': {
                'required': _('Please choose the file')
            }
        }

