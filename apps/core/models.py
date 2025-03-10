from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import BaseModel
from apps.core import consts


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


class Group(BaseModel):
    name = models.CharField("Название группы", max_length=255)
    description = models.TextField("Описание", blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_groups",
        verbose_name="Создан пользователем",
    )
    members = models.ManyToManyField(
        User, related_name="group_memberships", verbose_name="Участники группы", blank=True
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name


class Project(BaseModel):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Группа",
        null=True,
        blank=True,
    )
    name = models.CharField("Название проекта", max_length=255)
    description = models.TextField("Описание", blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_projects",
        verbose_name="Создан пользователем",
    )
    members = models.ManyToManyField(
        User, related_name="projects", verbose_name="Участники проекта", blank=True
    )
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name


class Task(BaseModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks", verbose_name="Проект"
    )
    title = models.CharField("Заголовок", max_length=255)
    description = models.TextField("Описание", blank=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        verbose_name="Назначен на",
    )
    priority = models.CharField(
        "Приоритет",
        max_length=255,
        choices=consts.TaskPriority.CHOICES,
        default=consts.TaskPriority.MEDIUM,
    )
    status = models.CharField(
        "Статус",
        max_length=255,
        choices=consts.TaskStatus.CHOICES,
        default=consts.TaskStatus.OPEN,
    )
    due_date = models.DateTimeField("Срок выполнения", null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks",
        verbose_name="Создан пользователем",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title


class Comment(BaseModel):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="comments", verbose_name="Задача"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name="Автор"
    )
    text = models.TextField("Текст комментария")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий от {self.author.fullname} к задаче {self.task.title}"


class Attachment(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="Задача",
        null=True,
        blank=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="Комментарий",
        null=True,
        blank=True,
    )
    file = models.FileField("Файл", upload_to="attachments/")
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="uploaded_attachments",
        verbose_name="Загружен пользователем",
    )

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

    def __str__(self):
        return f"Вложение к {self.task or self.comment}"
