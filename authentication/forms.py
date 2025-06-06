from django.forms import ModelForm
from .models import User, GENDER_CHOICES


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.gender in [2, 3]:
            self.fields['gender'].choices = [choice for choice in GENDER_CHOICES if choice[0] != 1]
