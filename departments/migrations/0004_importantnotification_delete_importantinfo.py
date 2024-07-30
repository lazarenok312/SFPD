# Generated by Django 5.0.7 on 2024-07-30 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0003_alter_role_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('message', models.TextField(verbose_name='Содержание')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Важная информация',
                'verbose_name_plural': 'Важная информация',
            },
        ),
        migrations.DeleteModel(
            name='ImportantInfo',
        ),
    ]
