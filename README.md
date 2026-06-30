# Chatbot Venezuela - Backend

Este es el backend del proyecto Chatbot Venezuela, desarrollado con **Django** (versión 6.0.6) y **Django Channels** (versión 4.3.2) para dar soporte a comunicación asíncrona / WebSockets.

---

## 📂 Estructura del Proyecto

Para que te familiarices con la estructura de archivos, aquí tienes una descripción de dónde está cada cosa:

```text
chatbot-vzla-backend/
├── .venv/                 # Entorno virtual de Python con las dependencias instaladas.
├── chatbot/               # La aplicación Django principal que manejará la lógica del chatbot.
│   ├── migrations/        # Historial de migraciones de base de datos para esta app.
│   ├── admin.py           # Configuración del panel de administración de Django.
│   ├── apps.py            # Configuración general de la app "chatbot".
│   ├── models.py          # Modelos de base de datos (ORMs).
│   ├── tests.py           # Pruebas unitarias de la app.
│   └── views.py           # Vistas/Controladores que procesan las peticiones HTTP.
├── config/                # Carpeta de configuración del proyecto Django global.
│   ├── settings.py        # Configuración general del proyecto (BD, apps instaladas, middleware, etc.).
│   ├── urls.py            # Enrutador principal del proyecto (las URLs que Django mapea).
│   ├── asgi.py            # Configuración para servidores ASGI (esencial para WebSockets/Channels).
│   └── wsgi.py            # Configuración para servidores WSGI (despliegue tradicional HTTP).
├── db.sqlite3             # Base de datos SQLite local para desarrollo rápido.
├── manage.py              # Script de entrada para comandos de Django.
└── LICENSE                # Licencia del proyecto.
```

---

## 🛠️ Cómo Empezar (Setup Local)

Sigue estos pasos para arrancar el servidor de desarrollo localmente:

### 1. Activar el Entorno Virtual
El entorno virtual ya viene preparado en la carpeta `.venv`. Dependiendo de tu sistema operativo, actívalo con:

- **Linux/macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 2. Instalar Dependencias (opcional)
Las dependencias actuales son mínimas: `Django` y `channels`. Si necesitas instalar o reinstalar:
```bash
pip install django channels
```
*(Nota: Actualmente las dependencias instaladas en el entorno son `Django==6.0.6` y `channels==4.3.2`).*

### 3. Aplicar Migraciones
Django utiliza migraciones para sincronizar tus modelos de Python con la base de datos (SQLite en este caso):
```bash
python manage.py migrate
```

### 4. Crear un Superusuario (para el panel admin)
Para poder iniciar sesión en el panel administrador (`/admin`):
```bash
python manage.py createsuperuser
```
Sigue las instrucciones en la terminal para definir usuario, correo y contraseña.

### 5. Iniciar el Servidor de Desarrollo
```bash
python manage.py runserver
```
El servidor estará corriendo en `http://127.0.0.1:8000/`.

---

## 🚀 Guía Rápida de Django para Principiantes

Django sigue el patrón **MVT (Model-View-Template)** (una variante de MVC):

1. **Modelos (`models.py`)**: Aquí defines las tablas de la base de datos usando clases de Python.
2. **Vistas (`views.py`)**: Reciben una petición web (request) y devuelven una respuesta (response), generalmente en formato JSON para APIs, o renderizan plantillas.
3. **URLs (`urls.py`)**: Mapean rutas de URL (ej. `/api/chat/`) a funciones o clases en tus vistas.

### Flujo de Trabajo Típico en Django:

#### Paso 1: Registrar tu App
Para que Django reconozca la aplicación `chatbot`, debes añadirla a `INSTALLED_APPS` dentro del archivo `config/settings.py` (línea 33):
```python
INSTALLED_APPS = [
    ...
    'chatbot',  # Añade esto aquí
]
```

#### Paso 2: Crear un Modelo
Si necesitas almacenar conversaciones en la base de datos, edita `chatbot/models.py`:
```python
from django.db import models

class Message(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message[:20]}..."
```

Una vez creado o modificado un modelo, debes avisar a Django para que cree y aplique los cambios a la base de datos:
```bash
python manage.py makemigrations chatbot
python manage.py migrate
```

#### Paso 3: Crear una Vista
Si quieres exponer un endpoint HTTP, ve a `chatbot/views.py`:
```python
from django.http import JsonResponse
from .models import Message

def chat_history(request):
    messages = Message.objects.all().values('user_message', 'bot_response', 'created_at')
    return JsonResponse(list(messages), safe=False)
```

#### Paso 4: Enrutar la Vista
Primero, crea un archivo `chatbot/urls.py` para tu aplicación:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.chat_history, name='chat_history'),
]
```

Y luego inclúyelo en el archivo de rutas principal `config/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chatbot.urls')),  # Las URLs de chatbot empezarán por /api/
]
```

Ahora, al acceder a `http://127.0.0.1:8000/api/history/` verás el listado de mensajes en formato JSON.

---

## ⚡ Conexión con WebSockets (Django Channels)
Dado que el proyecto incluye `channels`, eventualmente configuraremos conexiones WebSockets para chat en tiempo real en lugar de polling HTTP.
- Toda la configuración de enrutamiento asíncrono se realiza configurando `config/asgi.py` y creando archivos de tipo `consumers.py` (los equivalentes asíncronos a las `views.py` clásicas).
