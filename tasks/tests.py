from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskModelTest(APITestCase):
    """Pruebas unitarias del modelo Task."""

    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='clave123')

    def test_crear_tarea_valores_por_defecto(self):
        tarea = Task.objects.create(title='Tarea 1', created_by=self.user)
        self.assertEqual(tarea.status, Task.Status.PENDING)
        self.assertEqual(tarea.priority, Task.Priority.MEDIUM)

    def test_str_de_la_tarea(self):
        tarea = Task.objects.create(title='Diseñar logo', created_by=self.user)
        self.assertIn('Diseñar logo', str(tarea))


class TaskAPITest(APITestCase):
    """Pruebas de integración de los endpoints de la API."""

    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='clave123')
        # Autenticamos al cliente para todas las peticiones
        self.client.force_authenticate(user=self.user)

    def test_crear_tarea(self):
        data = {
            'title': 'Nueva tarea',
            'description': 'Descripción',
            'priority': 'HIGH',
            'status': 'PENDING',
            'assigned_to': self.user.id,
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(response.data['created_by'], self.user.id)

    def test_listar_tareas(self):
        Task.objects.create(title='T1', created_by=self.user)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_actualizar_tarea(self):
        tarea = Task.objects.create(title='T1', created_by=self.user)
        response = self.client.patch(
            f'/api/tasks/{tarea.id}/', {'status': 'DONE'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tarea.refresh_from_db()
        self.assertEqual(tarea.status, 'DONE')

    def test_eliminar_tarea(self):
        tarea = Task.objects.create(title='T1', created_by=self.user)
        response = self.client.delete(f'/api/tasks/{tarea.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_filtrar_por_estado(self):
        Task.objects.create(title='T1', status='DONE', created_by=self.user)
        Task.objects.create(title='T2', status='PENDING', created_by=self.user)
        response = self.client.get('/api/tasks/?status=DONE')
        self.assertEqual(response.data['count'], 1)

    def test_filtrar_por_prioridad(self):
        Task.objects.create(title='T1', priority='HIGH', created_by=self.user)
        Task.objects.create(title='T2', priority='LOW', created_by=self.user)
        response = self.client.get('/api/tasks/?priority=HIGH')
        self.assertEqual(response.data['count'], 1)

    def test_acceso_sin_autenticacion_rechazado(self):
        # Quitamos la autenticación para esta prueba
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRegistrationTest(APITestCase):
    """Pruebas del registro de usuarios."""

    def test_registro_usuario(self):
        data = {'username': 'nuevo', 'email': 'n@x.com', 'password': 'clave123'}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='nuevo').exists())

    def test_login_devuelve_token(self):
        User.objects.create_user(username='ana', password='clave123')
        response = self.client.post(
            '/api/login/', {'username': 'ana', 'password': 'clave123'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)