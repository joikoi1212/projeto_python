# Generated by Django 5.1.7 on 2025-03-09 17:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20250309_1540'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='planchoices',
            old_name='external_plan_id',
            new_name='external_plan',
        ),
        migrations.RenameField(
            model_name='planchoices',
            old_name='plan',
            new_name='plan_code',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='const',
            new_name='cost',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='payment_provider_id',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='plan',
        ),
        migrations.AddField(
            model_name='subscription',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='subscription',
            name='external_subscription_id',
            field=models.CharField(default='', max_length=255, verbose_name='External subscription id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='plan_choice',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='client.planchoices'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
