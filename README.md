# SmartSales CRM - Modo Simple

¡Bienvenido a SmartSales CRM, una solución simple y efectiva para la gestión de ventas! Este proyecto es un sistema de CRM (Customer Relationship Management) desarrollado para ayudarte a registrar y gestionar tus ventas de manera eficiente.

## ¿Qué hace el proyecto?

SmartSales CRM permite:

*   **Registrar Ventas:** Guarda información esencial sobre cada venta, incluyendo el cliente y el monto.
*   **Gestión Simple:** Proporciona una interfaz (API REST) para interactuar con tus datos de ventas.

Es una base sólida para construir aplicaciones más complejas de gestión de clientes.

## Tecnologías Utilizadas

Este proyecto está construido con una pila de tecnologías modernas y robustas:

*   **FastAPI:** Un framework web de alto rendimiento para construir APIs en Python, conocido por su velocidad y facilidad de uso.
*   **SQLAlchemy:** Un potente ORM (Object Relational Mapper) para Python que facilita la interacción con bases de datos relacionales, proporcionando una abstracción de la base de datos.
*   **PostgreSQL:** Un sistema de gestión de bases de datos relacional de código abierto, robusto y escalable, utilizado para almacenar los datos de las ventas.
*   **Docker & Docker Compose:** Utilizado para empaquetar la aplicación y sus dependencias en contenedores, facilitando el despliegue y la gestión del entorno de desarrollo y producción.
*   **Uvicorn:** Un servidor ASGI de alta velocidad para FastAPI.

## Comandos para Clonar y Levantar el Proyecto

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

### 1. Clonar el Repositorio

Abre tu terminal y ejecuta el siguiente comando para clonar el repositorio de GitHub:

```bash
git clone <URL_DEL_REPOSITORIO>
cd SmartSales-CRM
```

**Nota:** Reemplaza `<URL_DEL_REPOSITORIO>` con la URL real de tu repositorio de GitHub.

### 2. Configuración del Entorno

Crea un archivo `.env` en la raíz del proyecto (al mismo nivel que `docker-compose.yml`) con la siguiente variable:

```
DATABASE_URL="postgresql://user:password@db:5432/salesdb"
```

Asegúrate de reemplazar `user`, `password` y `salesdb` con los valores que configures en tu `docker-compose.yml` si los cambias.

### 3. Levantar la Aplicación con Docker Compose

Una vez que tengas el archivo `.env` configurado, puedes levantar la aplicación y la base de datos utilizando Docker Compose:

```bash
docker-compose up -d
```

Este comando construirá las imágenes de Docker (si no existen) y levantará los servicios en segundo plano (`-d`).

### 4. Ejecutar Migraciones de la Base de Datos (si aplicas Alembic)

Si estás utilizando Alembic para gestionar las migraciones de la base de datos, necesitarás ejecutar las migraciones después de levantar los servicios. (Asumo que tienes un servicio para esto en tu `docker-compose.yml` o que las ejecutas manualmente).

**Ejemplo de comando para migraciones (ajusta según tu configuración):**

```bash
docker-compose exec backend alembic upgrade head
```

**Nota:** El comando `alembic upgrade head` aplicará todas las migraciones pendientes. Asegúrate de que tu servicio `backend` esté configurado para ejecutar Alembic.

### 5. Acceder a la API

Una vez que la aplicación esté en funcionamiento, podrás acceder a la API de FastAPI. Por defecto, estará disponible en:

`http://localhost:8000`

Puedes probar los endpoints como `/` y `/crear-venta/` utilizando herramientas como Postman, Insomnia o `curl`. La documentación interactiva de Swagger UI estará disponible en `http://localhost:8000/docs`.

---
