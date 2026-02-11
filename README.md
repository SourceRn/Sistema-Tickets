# Sistema de Gestión de Tickets (Service Desk MVP)

Sistema de seguimiento de incidentes y requerimientos desarrollado en Django. Este proyecto implementa una arquitectura modular y escalable, separando la lógica de negocio, la capa de acceso a datos y la interfaz de usuario, siguiendo principios de **Clean Architecture** y **Domain-Driven Design (DDD)** adaptado a Django.

## Características Principales

* **Gestión de Tickets:** Creación, asignación, seguimiento y cierre de incidentes.
* **Carga Masiva (Excel):** Importación de tickets desde archivos Excel con validación de datos y detección de duplicados.
* **Reportes:** Exportación inteligente de datos a Excel, incluyendo campos dinámicos (JSON).
* **Comentarios Anidados:** Hilo de conversación con soporte para adjuntar imágenes.
* **Búsqueda Avanzada:** Filtrado por texto, estado y asignación (Lógica acumulativa).
* **Seguridad:** Roles diferenciados (Superusuario, Staff, Usuario final) y protección CSRF.

## Arquitectura del Proyecto

El proyecto se aleja de la estructura monolítica por defecto de Django para adoptar una organización por capas:

### 1. Separación Frontend / Backend
* **`apps/`**: Contiene exclusivamente código Python (Lógica de Backend).
* **`resources/`**: Contiene HTML, CSS, JS e imágenes estáticas (Capa de Presentación).

### 2. Patrones de Diseño Implementados
Dentro de la aplicación `tickets`, se utilizan patrones específicos para mantener las vistas limpias ("Skinny Views"):

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