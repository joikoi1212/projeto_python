# Generated by Django 5.1.7 on 2025-03-09 15:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=2, unique=True, verbose_name='Plan code')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Plan name')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Cost')),
                ('is_active', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_changed', models.DateTimeField(default=django.utils.timezone.now)),
                ('description1', models.CharField(max_length=300, verbose_name='Plan description 1:')),
                ('description2', models.CharField(max_length=300, verbose_name='Plan description 2:')),
                ('external_plan_id', models.CharField(max_length=255, unique=True, verbose_name='External Plan ID')),
                ('external_api_url', models.CharField(max_length=2000, unique=True, verbose_name='External API URL')),
                ('external_style_json', models.CharField(max_length=2000, unique=True, verbose_name='External style JSON')),
            ],
        ),
        migrations.AlterField(
            model_name='subscription',
            name='const',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Plan Cost'),
        ),
    ]
