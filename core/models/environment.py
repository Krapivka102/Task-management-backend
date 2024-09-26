from django.db import models


class Environment(models.Model):
    name = models.CharField('Название окружения', max_length=200)
    description = models.TextField('Описание окружения', blank=True)
    owner = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='owned_environments')

    class Meta:
        verbose_name = 'Окружение'
        verbose_name_plural = 'Окружения'

class Project(models.Model):
    title = models.CharField('Заголовок проекта', max_length=200)
    description = models.TextField('Описание проекта', blank=True)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='projects')
    members = models.ManyToManyField('core.User', blank=True, through='ProjectMembership')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class ProjectMembership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    member = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField('Роль в проекте', max_length=20, choices=[
        ('owner', 'Владелец'),
        ('admin', 'Администратор'),
        ('member', 'Участник'),
    ], default='member')

    class Meta:
        verbose_name = 'Участвующий в проекте'
        verbose_name_plural = 'Участвующие в проекте'

class Task(models.Model):
    title = models.CharField('Заголовок задачи', max_length=200)
    description = models.TextField('Описание задачи')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    status = models.CharField('Статус задачи', max_length=20, choices=[
        ('todo', 'В работе'),
        ('in_progress', 'В процессе'),
        ('done', 'Завершено'),
    ], default='todo')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class Comment(models.Model):
    content = models.TextField('Содержание комментария')
    author = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey('core.Task', on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Attachment(models.Model):
    file = models.FileField('Файл вложения', upload_to='task_manager/attachments/')
    description = models.CharField('Описание файла', max_length=255)
    uploaded_by = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='uploaded_attachments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'