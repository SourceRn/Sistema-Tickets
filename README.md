# Sistema de Gestión de Tickets (Service Desk MVP)

Sistema de seguimiento de incidentes y requerimientos desarrollado en Django. Este proyecto implementa una arquitectura modular y escalable, diseñada para entornos corporativos mediante **contenedores**

## Características Principales

* **Infraestructura Robusta** Orquestación con Docker (Nginx + Gunicorn + PostgreSQL).
* **Gestión de Tickets** Creación, asignación, seguimiento y cierre de incidentes.
* **Carga Masiva (Excel)** Importación de tickets con validación y detección de duplicados.
* **Seguridad:** Roles diferenciados, protección CSRF y aislamiento de red entre contenedores.

## Despliegue con Docker (Producción)

Forma recomendada de ejecutar el sistema. Asegura que el entorno sea idéntico en desarrollo y producción.

### 1. Preparación

Configuración de variables de entorno copiando el archivo de ejemplo.

<pre> ```bash cp .env.example .env ``` </pre>

### 2. Encendido del Sistema
El siguiente comando construye las imágenes, crea los volúmenes de datos y levanta los servicios en segundo plano:

<pre> ```bash docker-compose up -d --build ``` </pre>

### 3. Configuración inicial (Primer acceso)
Se debe crear el usaurio administrador inicial.

<pre> ```bash docker-compose exec web python manage.py createsuperuser ``` </pre>

Ahora se puede acceder en: <pre> ```http://localhost``` </pre>

## Comandos de Mantenimiento
**Ver Logs en tiempo real:** <pre> ```bash docker-compose logs -f web nginx ``` </pre>
**Apagar el sistema:** <pre> ```bash docker-compose down ``` </pre>
**Aplicar cambios en el código:** <pre> ```bash docker-compose up -d --build ``` </pre> (docker detecta cambios y reconstruye solo lo necesario)
**Recolectar estáticos manualmente:** <pre> ```bash docker-compose exec web python manage.py collectstatic --noinput ``` </pre>

## Arquitectura del proyecto
PROYECTO_RAIZ/
├── config/             # Configuraciones globales (settings, urls, wsgi)
├── apps/               # Lógica de Negocio (Backend)
│   └── tickets/        # Aplicación principal de gestión
├── resources/          # Capa de Presentación (Frontend)
│   ├── static/         # CSS, JS fuente
│   └── templates/      # Plantillas HTML
├── nginx/              # Configuración del servidor Web Proxy
│   └── default.conf
├── staticfiles/        # Destino final de estáticos (Generado por collectstatic)
├── media/              # Archivos subidos (Evidencias de tickets)
├── .env.example        # Plantilla de configuración (Zero Hardcoding)
├── docker-compose.yml  # Orquestador de servicios (Nginx, Web, DB)
├── Dockerfile          # Receta de construcción de la imagen Python
├── entrypoint.sh       # Script de automatización de migraciones y arranque
├── manage.py           # Utilidad de administración de Django (Entrypoint)
└── requirements.txt    # Dependencias del proyecto (incluye Gunicorn)

### Explicación Arquitectónica (Infraestructura)
Se adoptó la **Estrategia de 3 Capas**:
**1. Nginx.** Actúa como Reverse Proxy y servidor de archivos estáticos/media, liberando Django de tareas de E/S
**2. Gunicorn.** Servidor WSGI de alto rendimiento que maneja los procesos de python.
**3. PostgreSQL.** Base de datos relacional aislada en una red privada de Docker, accesible solo por la aplicación.















* **Services (`services.py`):** Manejan la lógica de negocio compleja y transacciones (ej. Procesamiento de Excel).
* **Selectors (`selectors.py`):** Encapsulan consultas complejas a la base de datos (QuerySets) para ser reutilizadas.
* **Modular Views (`views/`):** Las vistas están divididas por dominio (`tickets.py`, `export_import.py`, `comments.py`) en lugar de un archivo gigante.
* **Constantes Centralizadas (`constants.py`):** Uso de `TextChoices` para evitar "Strings Mágicos".

## Estructura de Carpetas

```text
PROYECTO_RAIZ/
├── config/                 # Configuraciones globales (settings, urls, wsgi)
├── apps/                   # Lógica de Negocio (Backend)
│   └── tickets/
│       ├── migrations/
│       ├── tests/          # Pruebas unitarias organizadas
│       ├── views/          # Controladores modulares
│       │   ├── tickets.py
│       │   ├── export_import.py
│       │   └── comments.py
│       ├── models.py       # Definición de datos
│       ├── services.py     # Lógica de escritura/negocio
│       ├── selectors.py    # Lógica de lectura
│       ├── forms.py        # Validación de entrada
│       └── constants.py    # Enumeraciones
│
├── resources/              # Capa de Presentación (Frontend)
│   ├── static/             # CSS, JS, Imágenes del sistema
│   └── templates/
│       ├── registration/   # Login/Logout
│       └── tickets/        # Plantillas de la app
│
├── media/                  # Archivos subidos por usuarios
├── manage.py
└── requirements.txt