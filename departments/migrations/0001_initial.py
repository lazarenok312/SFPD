# Generated by Django 5.0.7 on 2024-07-31 08:18

import departments.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
            ],
            options={
                'verbose_name': 'История изменений',
                'verbose_name_plural': 'Истории изменений',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ContractServiceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Статус контракта')),
            ],
            options={
                'verbose_name': 'Статус контракта',
                'verbose_name_plural': 'Статус контракта',
            },
        ),
        migrations.CreateModel(
            name='CPDPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('chief', 'Chief of CPD'), ('dep_chief1', 'Dep.Chief of CPD'), ('dep_chief2', 'Dep.Chief of CPD')], max_length=10, verbose_name='Должность')),
                ('nickname', models.CharField(max_length=100, verbose_name='Ник')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='cpd_photos/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Должность CPD',
                'verbose_name_plural': 'Должности CPD',
            },
        ),
        migrations.CreateModel(
            name='DBPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('head', 'Head of DB'), ('dep_head1', 'Dep.Head of DB'), ('dep_head2', 'Dep.Head of DB')], max_length=10, verbose_name='Должность')),
                ('nickname', models.CharField(max_length=100, verbose_name='Ник')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='db_photos/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Должность DB',
                'verbose_name_plural': 'Должности DB',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Отдел')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
            },
        ),
        migrations.CreateModel(
            name='DepartmentStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('title', models.CharField(choices=[('sheriff', 'Шериф департамента'), ('colonel1', 'Полковник1'), ('colonel2', 'Полковник2'), ('colonel3', 'Полковник3'), ('lcolonel1', 'Подполковник1'), ('lcolonel2', 'Подполковник2'), ('lcolonel3', 'Подполковник3'), ('major1', 'Майор1'), ('major2', 'Майор2'), ('major3', 'Майор3'), ('major4', 'Майор4')], max_length=100, verbose_name='Звание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='department_staff', verbose_name='Фото')),
                ('job_title', models.TextField(blank=True, max_length=50, null=True, verbose_name='Должность')),
                ('discord_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на Discord')),
                ('vk_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на VK')),
            ],
            options={
                'verbose_name': 'Штаб',
                'verbose_name_plural': 'Штаб',
            },
        ),
        migrations.CreateModel(
            name='ImportantNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('message', models.TextField(verbose_name='Содержание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Важная информация',
                'verbose_name_plural': 'Важная информация',
            },
        ),
        migrations.CreateModel(
            name='PoliceAcademyPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('chief', 'Chief of PA'), ('dep_chief1', 'Dep.Chief of PA'), ('dep_chief2', 'Dep.Chief of PA')], max_length=10, verbose_name='Должность')),
                ('nickname', models.CharField(max_length=100, verbose_name='Ник')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='police_academy_photos/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Должность ПА',
                'verbose_name_plural': 'Должности ПА',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
            ],
            options={
                'verbose_name': 'Подписки на рассылку',
                'verbose_name_plural': 'Подписки на рассылку',
            },
        ),
        migrations.CreateModel(
            name='SWATPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('commander', 'Сommander of SWAT'), ('dep_commander1', 'Dep. Commander of SWAT'), ('dep_commander2', 'Dep. Commander of SWAT')], max_length=20, verbose_name='Должность')),
                ('nickname', models.CharField(max_length=100, verbose_name='Ник')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='swat_photos/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Должность SWAT',
                'verbose_name_plural': 'Должности SWAT',
            },
        ),
        migrations.CreateModel(
            name='UnsubscribeToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('token', models.CharField(default=departments.models.generate_token, max_length=64, unique=True, verbose_name='Токен')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Токен отписки',
                'verbose_name_plural': 'Токен отписки',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Должность')),
                ('order', models.IntegerField(blank=True, default=0, verbose_name='Порядок')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departments.department', verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ['department', 'order'],
                'unique_together': {('department', 'name')},
            },
        ),
    ]
