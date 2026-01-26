# 🎫 Sistema de Gestión de Tickets (Django)

Un sistema de gestión de incidentes robusto y minimalista diseñado para equipos de soporte. Permite la importación masiva de tickets desde Excel, asignación inteligente de tareas y un flujo de trabajo claro para agentes de servicio.

## 🚀 Características Principales

* **Importación Masiva:** Carga cientos de tickets arrastrando un archivo Excel. El sistema limpia y normaliza los datos automáticamente.
* **Gestión de Estados:** Flujo lógico de tickets: *Pendiente* ➝ *En Proceso* ➝ *Finalizado*.
* **Prevención de Colisiones:** Bloqueo de tickets. Si el Agente A está trabajando en un ticket, el Agente B no puede intervenir, evitando duplicidad de esfuerzos.
* **Seguridad por Roles:** Diferenciación estricta entre Superusuarios (Administradores) y Agentes.
* **Interfaz Responsiva:** Diseño adaptado para móviles y escritorio utilizando Bootstrap 5.
* **Protección de Rutas:** Middleware personalizado y validaciones para proteger el panel de administración y las rutas de carga.

---

## 📂 Arquitectura del Proyecto

A continuación se describe la función de los archivos clave mostrados en la estructura del proyecto:

### 📁 Raíz
* **`manage.py`**: El script maestro de Django para ejecutar el servidor, crear migraciones y gestionar usuarios.
* **`db.sqlite3`**: Base de datos ligera y portable (ver sección Base de Datos).

### 📁 config (Configuración Global)
* **`settings.py`**: Configuración del núcleo (Base de datos, Apps instaladas, Seguridad, Archivos Estáticos).
* **`urls.py`**: El "mapa" de entrada. Aquí se define la ruta segura para el admin y se incluyen las rutas de la app de tickets.

### 📁 tickets (La Aplicación Principal)
* **`models.py`**: Define la estructura de datos. Aquí vive la clase `Ticket` (título, descripción, fechas) y el campo flexible JSON para datos extra del Excel.
* **`views.py`**: El cerebro del sistema. Contiene la lógica para:
    * Leer y limpiar el Excel con Pandas.
    * Filtrar y buscar tickets.
    * Controlar la lógica de "Tomar", "Soltar" y "Finalizar" tareas.
* **`urls.py`**: Define las rutas internas (ej: `/subir`, `/tomar/<id>`).
* **`middleware.py`**: Capa de seguridad extra que intercepta las peticiones para proteger rutas sensibles o el panel de admin.
* **`templates/tickets/`**:
    * `lista.html`: Dashboard principal con filtros y paginación.
    * `detalle.html`: Vista profunda del ticket con acciones de gestión.
    * `subir.html`: Formulario de carga de Excel.

---

## 👥 Roles y Permisos

El sistema maneja dos niveles de autoridad:

### 1. Superusuario (Administrador)
* **Capacidad exclusiva:** Puede ver y acceder a la opción "Importar Excel" en el menú de navegación.
* **Acceso Total:** Tiene acceso al panel de administración de Django (ruta segura).
* **Visibilidad:** Puede ver el dashboard completo.

### 2. Agente (Usuario Staff/Normal)
* **Gestión de Tickets:** Puede buscar, filtrar y "Tomar" tickets disponibles.
* **Restricciones:**
    * No ve la opción de importar Excel.
    * No tiene acceso al panel de administración (recibe un error 404 si intenta entrar).
    * No puede ver los detalles de un ticket que ya está asignado a otro compañero (Privacidad entre agentes).
* **Acciones:** Puede "Finalizar" sus tickets o "Soltar" un ticket si no puede resolverlo, devolviéndolo a la lista general.

---

## 💾 Base de Datos (SQLite)

El proyecto utiliza **SQLite 3**, que viene integrado por defecto en Django.

* **¿Cómo funciona?**: Toda la información (Usuarios, Tickets, Sesiones) se guarda en el archivo `db.sqlite3`.
* **Ventajas**:
    * **Portabilidad**: No requiere instalar servidores SQL externos (como MySQL o PostgreSQL).
    * **Backup**: Hacer una copia de seguridad es tan simple como copiar el archivo `db.sqlite3`.
    * **Despliegue**: Ideal para entornos de desarrollo y pequeñas implementaciones internas.

---

## 🛠️ Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone <tu-url-del-repo>

2. **Crear Entorno Virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate # En Windows: venv\Scripts\activate

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt

4. **Aplicar migraciones (crear la BD):**
   ```bash
   python manage.py migrate

5. **Crear Superusuario:**
   ```bash
   python manage.py createsuperuser  

6. **Ejecutar el servidor:**
   ```bash
   python manage.py runserver