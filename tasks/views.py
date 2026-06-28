from rest_framework import viewsets

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de tareas.

    Operaciones automaticas:
      - GET    /api/tasks/        -> listar (leer)
      - POST   /api/tasks/        -> crear
      - GET    /api/tasks/{id}/   -> detalle (leer)
      - PUT    /api/tasks/{id}/   -> actualizar completo
      - PATCH  /api/tasks/{id}/   -> actualizar parcial
      - DELETE /api/tasks/{id}/   -> eliminar

    Filtros (consulta de tareas):
      ?assigned_to=<id>  ?status=<estado>  ?priority=<prioridad>
      ?search=<texto>    ?ordering=<campo>
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # Filtro por usuario asignado, estado o prioridad
    filterset_fields = ['assigned_to', 'status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority', 'status']

    def perform_create(self, serializer):
        # Asigna automaticamente el creador al usuario autenticado
        serializer.save(created_by=self.request.user)
