# Generated by Django 5.0.7 on 2024-07-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0002_alter_department_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'Должность', 'verbose_name_plural': 'Должности'},
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Отдел'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Должность'),
        ),
    ]
