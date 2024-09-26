from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    patronymic = models.CharField('отчество', max_length=255, blank=True)
    fullname = models.CharField('ФИО', max_length=255, blank=True)
    is_system = models.BooleanField('системный пользователь', default=False)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def save(self, *args, **kwargs) -> None:
        self.fullname = ' '.join(filter(bool, (self.last_name, self.first_name, self.patronymic)))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.get_full_name() or self.username
