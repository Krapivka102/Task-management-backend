from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import BaseModel


class User(BaseModel, AbstractUser):
    patronymic = models.CharField("Отчество", max_length=255, blank=True)
    fullname = models.CharField("ФИО", max_length=255, blank=True)
    is_system = models.BooleanField("Системный пользователь", default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args: tuple, **kwargs: dict) -> None:
        self.fullname = " ".join(
            filter(bool, (self.last_name, self.first_name, self.patronymic))
        )
        super().save(*args, **kwargs)
