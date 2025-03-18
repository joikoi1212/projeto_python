from django.contrib import admin
from .models import Subscription, PlanChoices
# Register your models here.

admin.site.register(Subscription)
admin.site.register(PlanChoices)