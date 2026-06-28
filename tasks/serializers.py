from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializa tareas. Muestra etiquetas legibles para prioridad y estado."""

    priority_display = serializers.CharField(
        source='get_priority_display', read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )
    assigned_to_username = serializers.CharField(
        source='assigned_to.username', read_only=True
    )
    created_by_username = serializers.CharField(
        source='created_by.username', read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'priority',
            'priority_display',
            'status',
            'status_display',
            'assigned_to',
            'assigned_to_username',
            'created_by',
            'created_by_username',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('El titulo no puede estar vacio.')
        return value
