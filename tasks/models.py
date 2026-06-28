from django.conf import settings
from django.db import models


class Task(models.Model):
    """Tarea colaborativa gestionada dentro de un equipo de trabajo."""

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Baja'
        MEDIUM = 'MEDIUM', 'Media'
        HIGH = 'HIGH', 'Alta'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        IN_PROGRESS = 'IN_PROGRESS', 'En progreso'
        DONE = 'DONE', 'Completada'

    title = models.CharField('Titulo', max_length=200)
    description = models.TextField('Descripcion', blank=True)
    priority = models.CharField(
        'Prioridad',
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    status = models.CharField(
        'Estado',
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='Usuario asignado',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Creado por',
    )
    created_at = models.DateTimeField('Creado el', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado el', auto_now=True)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'
