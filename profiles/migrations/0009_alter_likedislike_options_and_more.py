# Generated by Django 5.0.7 on 2024-07-19 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_alter_profilechangelog_options_profile_dislikes_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likedislike',
            options={'verbose_name': 'Лайки Дизлайки', 'verbose_name_plural': 'Лайки Дизлайки'},
        ),
        migrations.AlterUniqueTogether(
            name='likedislike',
            unique_together=set(),
        ),
    ]
