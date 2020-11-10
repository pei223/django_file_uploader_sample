from django import forms
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from app.utils.validators import FileSizeValidator


class UserProfileForm(forms.Form):
    intro = forms.CharField(widget=forms.Textarea, initial="", required=False, validators=[MaxLengthValidator(500)])
    thumbnail = forms.FileField(
        validators=[FileExtensionValidator(["png", "jpeg", "jpg", "bmp"]), FileSizeValidator(val=5, byte_type="mb")],
        required=False,
    )
    is_thumbnail_delete = forms.BooleanField(initial=False, required=False)
