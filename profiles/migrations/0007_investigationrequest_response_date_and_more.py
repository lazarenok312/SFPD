# Generated by Django 4.2.13 on 2024-08-24 12:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_investigationrequest_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigationrequest',
            name='response_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата ответа'),
        ),
        migrations.AddField(
            model_name='investigationrequest',
            name='response_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responses', to='profiles.profile', verbose_name='Профиль ответившего'),
        ),
        migrations.AlterField(
            model_name='investigationrequest',
            name='phone_number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^\\d{3}-\\d{3}(-\\d{1,3})?$', 'Номер телефона должен содержать от 4 до 6 цифр, возможно с тире.')], verbose_name='Телефон'),
        ),
    ]
