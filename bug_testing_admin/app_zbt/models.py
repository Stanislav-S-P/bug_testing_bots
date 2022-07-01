from django.db import models


class BugReport(models.Model):
    user_id = models.BigIntegerField(verbose_name='id пользователя')
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    device_model = models.CharField(max_length=150, verbose_name='Модель девайса')
    periodicity = models.TextField(verbose_name='Частота')
    type_of_problem = models.CharField(max_length=50, verbose_name='Тип проблемы')
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Баг репорт'
        verbose_name_plural = 'Баг репорты'
        db_table = 'zbt_bug_report'


class UserPhone(models.Model):
    user_id = models.BigIntegerField(verbose_name='id пользователя')
    phone = models.CharField(max_length=25, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
        db_table = 'zbt_user_phone'


class FileReport(models.Model):
    report = models.ForeignKey(BugReport, related_name='file_report', on_delete=models.CASCADE, verbose_name='Репорт')
    file = models.FileField(upload_to='files/', null=True, blank=True)

    def __str__(self):
        return f"{self.report}"

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        db_table = 'zbt_file_report'


class UserProfile(models.Model):

    CHOICES = [
        ('Новый', 'Новый'),
        ('Активный', 'Активный'),
        ('Заблокирован', 'Заблокирован'),
    ]

    user_id = models.BigIntegerField(verbose_name='id пользователя')
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    device_model = models.CharField(max_length=150, verbose_name='Модель девайса')
    email = models.CharField(max_length=40, null=True, verbose_name='Электронная почта')
    login = models.CharField(max_length=40, verbose_name='Логин пользователя')
    password = models.CharField(max_length=200, verbose_name='Пароль')
    hash_password = models.CharField(max_length=400, verbose_name='Хэш пароль')
    status = models.CharField(max_length=20, choices=CHOICES, default='Новый', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        db_table = 'zbt_profile'
        ordering = ['-created_at']


class AdminProfile(models.Model):
    user_id = models.BigIntegerField(verbose_name='id администратора')

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
        db_table = 'zbt_admin'


class CommandActivity(models.Model):
    STATUS_CHOICES = [
        ('Закрыта', 'Закрыта'),
        ('Открыта', 'Открыта')
    ]
    command = models.CharField(max_length=20, verbose_name='Команда')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Закрыта', verbose_name='Статус')

    def __str__(self):
        return f"{self.command}"

    class Meta:
        verbose_name = 'Активация команды'
        verbose_name_plural = 'Активация команд'
        db_table = 'zbt_command'


class IPAddress(models.Model):
    ip_address = models.CharField(max_length=20, verbose_name='ip-адрес')

    def __str__(self):
        return f"{self.ip_address}"

    class Meta:
        verbose_name = 'IP адрес'
        verbose_name_plural = 'IP адреса'
        db_table = 'zbt_ip_address'
