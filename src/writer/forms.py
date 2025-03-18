from django.forms import ModelForm
from .models import Article
from common.django_utils import AsyncModelFormMixin
from account.models import CustomUser

class ArticleForm(ModelForm, AsyncModelFormMixin):
    class Meta:
        model = Article
        fields = (  
            'title',
            'content',
            'is_premium'  
        )
        
class UpdateUserForm(ModelForm, AsyncModelFormMixin):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
        )