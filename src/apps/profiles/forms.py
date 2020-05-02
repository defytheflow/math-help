from django import forms

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):

    error_messages = {
        'invalid_photo_size': (
            'Максимальный размер фотографии '
            f'{Profile.PHOTO_MAX_WIDTH} x {Profile.PHOTO_MAX_HEIGHT} пикселей.'
        )
    }

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'photo', 'gender', 'age']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        # If user uploads a new image
        if photo != self.instance.photo:
            # Check uploaded photo dimension
            width, height = get_image_dimensions(photo)
            if width > Profile.PHOTO_MAX_WIDTH or height > Profile.PHOTO_MAX_HEIGHT:
                raise ValidationError(self.error_messages['invalid_photo_size'])
            self.instance.delete_photo()
        return photo
