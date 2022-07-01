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
        db_table = 'bug_report'


class UserPhone(models.Model):
    user_id = models.BigIntegerField(verbose_name='id пользователя')
    phone = models.CharField(max_length=25, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
        db_table = 'user_phone'


class FileReport(models.Model):
    report = models.ForeignKey(BugReport, related_name='file_report', on_delete=models.CASCADE, verbose_name='Репорт')
    file = models.FileField(upload_to='files/', null=True, blank=True)

    def __str__(self):
        return f"{self.report}"

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        db_table = 'file_report'
