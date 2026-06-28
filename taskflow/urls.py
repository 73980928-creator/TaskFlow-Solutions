from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    # API de tareas (CRUD + filtros)
    path('api/', include('tasks.urls')),

    # API de usuarios (registro + listado)
    path('api/', include('users.urls')),

    # Autenticacion por token: POST username/password -> token
    path('api/login/', obtain_auth_token, name='api-login'),

    # Login navegable de DRF (util para probar en el navegador)
    path('api-auth/', include('rest_framework.urls')),
]
