from django.forms import ModelForm
from common.django_utils import AsyncModelFormMixin
from account.models import CustomUser


class UpdateUserForm(ModelForm, AsyncModelFormMixin):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
        )