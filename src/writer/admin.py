from django.contrib import admin
from . import models as writer_models
# Register your models here.

admin.site.register(writer_models.Article)
