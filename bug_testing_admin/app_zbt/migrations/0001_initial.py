# Generated by Django 4.0.5 on 2022-06-22 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='id администратора')),
            ],
            options={
                'verbose_name': 'Администратор',
                'verbose_name_plural': 'Администраторы',
                'db_table': 'zbt_admin',
            },
        ),
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='id пользователя')),
                ('username', models.CharField(max_length=50, verbose_name='Имя пользователя')),
                ('device_model', models.CharField(max_length=150, verbose_name='Модель девайса')),
                ('periodicity', models.TextField(verbose_name='Частота')),
                ('type_of_problem', models.CharField(max_length=50, verbose_name='Тип проблемы')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Баг репорт',
                'verbose_name_plural': 'Баг репорты',
                'db_table': 'zbt_bug_report',
            },
        ),
        migrations.CreateModel(
            name='UserPhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='id пользователя')),
                ('phone', models.CharField(max_length=25, verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Телефон',
                'verbose_name_plural': 'Телефоны',
                'db_table': 'zbt_user_phone',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='id пользователя')),
                ('username', models.CharField(max_length=50, verbose_name='Имя пользователя')),
                ('device_model', models.CharField(max_length=150, verbose_name='Модель девайса')),
                ('login', models.CharField(max_length=40, verbose_name='Логин пользователя')),
                ('password', models.CharField(max_length=200, verbose_name='Пароль')),
                ('hash_password', models.CharField(max_length=400, verbose_name='Хэш пароль')),
                ('status', models.CharField(choices=[('Новый', 'Новый'), ('Активный', 'Активный')], default='Новый', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
                'db_table': 'zbt_profile',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FileReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_report', to='app_zbt.bugreport', verbose_name='Репорт')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
                'db_table': 'zbt_file_report',
            },
        ),
    ]