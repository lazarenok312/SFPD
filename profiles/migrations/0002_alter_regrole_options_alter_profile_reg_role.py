# Generated by Django 5.0.7 on 2024-08-12 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='regrole',
            options={'verbose_name': 'Фракция', 'verbose_name_plural': 'Фракция'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='reg_role',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.regrole', verbose_name='Фракция'),
        ),
    ]
