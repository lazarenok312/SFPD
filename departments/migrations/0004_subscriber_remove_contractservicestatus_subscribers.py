# Generated by Django 4.2.13 on 2024-07-24 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0003_delete_subscription_delete_unsubscription_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='contractservicestatus',
            name='subscribers',
        ),
    ]
