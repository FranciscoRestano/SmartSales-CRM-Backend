# SmartSales CRM - Backend API

Bienvenido a **SmartSales CRM**, un backend robusto diseñado para la gestión de relaciones con clientes y ventas transaccionales. Este proyecto implementa una arquitectura profesional separando la lógica de negocio, la persistencia de datos y la gestión de esquemas.

## Características Técnicas

* **Arquitectura Relacional:** Modelado de datos con integridad referencial (Clientes <-> Ventas) usando **PostgreSQL**.
* **API RESTful:** Endpoints rápidos y documentados automáticamente con **FastAPI**.
* **Gestión de Esquemas:** Control de versiones de base de datos utilizando **Alembic** (Migrations).
* **Infraestructura:** Base de datos contenerizada con **Docker Compose**.
* **ORM:** Uso de **SQLAlchemy** para abstracción de base de datos segura.

## Tecnologías

* **Lenguaje:** Python 3.10+
* **Framework:** FastAPI + Uvicorn
* **Base de Datos:** PostgreSQL 15
* **ORM:** SQLAlchemy 2.0
* **Migraciones:** Alembic
* **Infraestructura:** Docker & Docker Compose

## Instalación y Configuración

Sigue estos pasos para levantar el entorno de desarrollo local.

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/FranciscoRestano/SmartSales-CRM-Backend.git](https://github.com/FranciscoRestano/SmartSales-CRM-Backend.git)
cd SmartSales-CRM-Backend
