from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _t
from account.models import CustomUser
# Create your models here.

TITLE_MAXLENGTH = 100
CONTENT_MAXLENGTH = 160

class Article(models.Model):
    title = models.CharField(max_length=TITLE_MAXLENGTH,verbose_name=_t('title'))
    content = models.TextField(max_length=CONTENT_MAXLENGTH,verbose_name=_t('content'))
    date_posted = models.DateTimeField(default=timezone.now)
    is_premium = models.BooleanField(default=False,verbose_name=_t('is premium article'))
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


