# Generated by Django 4.0.5 on 2022-06-15 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bug_testing', '0001_initial'),
    ]

    operations = [
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
                'db_table': 'user_phone',
            },
        ),
    ]