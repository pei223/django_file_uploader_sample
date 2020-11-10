from django import forms

from app.utils.validators import FileSizeValidator


class FileUploadForm(forms.Form):
    file = forms.FileField(
        validators=[FileSizeValidator(val=1, byte_type="gb")],
        required=True,
    )


class FileSelectForm(forms.Form):
    pk = forms.IntegerField()
