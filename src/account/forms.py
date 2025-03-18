from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from asgiref.sync import sync_to_async, async_to_sync

from .models import CustomUser
from common.django_utils import AsyncFormMixin, AsyncModelFormMixin

class CustomUserCreationForm(UserCreationForm, AsyncModelFormMixin):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_writer') 
        
class CustomAuthenticationForm(AuthenticationForm, AsyncFormMixin):
    pass