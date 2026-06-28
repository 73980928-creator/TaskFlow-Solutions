# TaskFlow-Solutions

API RESTful para gestionar tareas colaborativas dentro de un equipo de
trabajo. Permite registrar, asignar, actualizar, eliminar y consultar tareas.
Construida con **Django** y **Django REST Framework**.

## Tecnologias

- Python 3.12
- Django 6.0
- Django REST Framework 3.17
- django-filter (filtros de consulta)
- SQLite por defecto (PostgreSQL listo en `settings.py`)

## Instalacion

```bash
# 1. Clonar el repositorio
git clone https://github.com/73980928-creator/TaskFlow-Solutions.git
cd TaskFlow-Solutions

# 2. Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Aplicar migraciones
python manage.py migrate

# 4. (Opcional) crear superusuario para el admin
python manage.py createsuperuser

# 5. Levantar el servidor
python manage.py runserver
```

El servidor queda en `http://127.0.0.1:8000/`.

## Modelo de datos: Task

| Campo         | Tipo        | Descripcion                              |
|---------------|-------------|------------------------------------------|
| title         | CharField   | Titulo de la tarea                       |
| description   | TextField   | Descripcion                              |
| priority      | Choice      | LOW / MEDIUM / HIGH                      |
| status        | Choice      | PENDING / IN_PROGRESS / DONE            |
| assigned_to   | FK User     | Usuario asignado                         |
| created_by    | FK User     | Quien creo la tarea (automatico)         |
| created_at    | DateTime    | Fecha de creacion                        |
| updated_at    | DateTime    | Ultima actualizacion                     |

## Autenticacion

La API usa autenticacion por Token.

```bash
# Registrar usuario
POST /api/register/   { "username": "...", "email": "...", "password": "..." }

# Obtener token
POST /api/login/      { "username": "...", "password": "..." }
# -> { "token": "abc123..." }
```

Incluir el token en cada peticion protegida:
`Authorization: Token abc123...`

## Endpoints

| Metodo | Ruta                | Accion                          |
|--------|---------------------|---------------------------------|
| GET    | /api/tasks/         | Listar tareas (Read)            |
| POST   | /api/tasks/         | Crear tarea (Create)            |
| GET    | /api/tasks/{id}/    | Detalle de tarea (Read)         |
| PUT    | /api/tasks/{id}/    | Actualizar completo (Update)    |
| PATCH  | /api/tasks/{id}/    | Actualizar parcial (Update)     |
| DELETE | /api/tasks/{id}/    | Eliminar tarea (Delete)         |
| GET    | /api/users/         | Listar usuarios                 |

### Filtros de consulta

```
GET /api/tasks/?assigned_to=1      # por usuario asignado
GET /api/tasks/?status=PENDING     # por estado
GET /api/tasks/?priority=HIGH      # por prioridad
GET /api/tasks/?search=logo        # busqueda en titulo/descripcion
GET /api/tasks/?ordering=-created_at
```

## Cambiar a PostgreSQL

En `taskflow/settings.py` descomentar el bloque de PostgreSQL,
instalar el driver y volver a migrar:

```bash
pip install psycopg2-binary
python manage.py migrate
```
