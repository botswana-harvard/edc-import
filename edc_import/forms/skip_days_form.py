from django import forms
from ..models import UploadSkipDays


class SkipDaysForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super(SkipDaysForm, self).clean()
#         file_name = cleaned_data.get('transaction_file').name.replace('\\', '/').split('/')[-1]
#         if self._meta.model.objects.filter(file_name=file_name):
#             raise forms.ValidationError('A file with this name was uploaded in a previous session. Is this a duplicate or incorrectly named file? Got {0}'.format(file_name))
#         self.instance.check_for_transactions(cleaned_data.get('transaction_file'), forms.ValidationError)

        return cleaned_data
    
    class Meta:
            model = UploadSkipDays
