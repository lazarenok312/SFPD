# Generated by Django 5.0.7 on 2024-07-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Биография'),
        ),
    ]
