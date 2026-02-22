# 🚀 Job Searcher App (Rails 8 + Python Scrapers)

Una aplicación potente construida con **Ruby on Rails 8** que utiliza scripts de **Python (Playwright)** para buscar y centralizar vacantes de múltiples plataformas en tiempo real.

## ✨ Funcionalidades Principales

* **Multi-Plataforma Scraping**: Busca vacantes automáticamente en:
  * **Indeed** 🔍
  * **Computrabajo** (con soporte para puntajes de empresas) ⭐
  * **El Empleo** 🇨🇴
  * **LinkedIn** (Búsqueda pública, sin necesidad de login) 🌐
* **Gestión de Aplicaciones**:
  * Filtra trabajos por título, empresa o puntaje.
  * Sistema de **Estados**: Marca vacantes como *Pendiente*, *Aplicado*, *Rechazado* o *Ignorado*.
  * Vista limpia: Los trabajos ignorados se ocultan automáticamente.
* **Reportes y Exportación**:
  * Genera reportes en **Excel (.xlsx)** y **CSV**.
  * Nomenclatura inteligente con timestamp (`jobs-YYYYMMDD_HHMMSS`) para evitar duplicados.
  * Las exportaciones respetan los filtros aplicados en la web.
* **Automatización**:
  * Procesamiento en segundo plano con **Solid Queue**.
  * **Tarea Recurrente**: Limpieza automática de vacantes con más de una semana de antigüedad (ejecutada diariamente a las 3:00 AM).
* **Interfaz Moderna**: Construida con Bootstrap 5, diseño responsivo y notificaciones Turbo.

## 🛠️ Requisitos del Sistema

* **Ruby**: 3.2.2+
* **Python**: 3.10+ (dentro de un entorno virtual `./venv`)
* **Node.js**: Para compilación de CSS (Bootstrap)
* **PostgreSQL**: Base de datos principal.

## 🚀 Instalación y Configuración

1. **Clonar y Dependencias**:

    ```bash
    bundle install
    npm install
    # Configurar venv de python
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
    ```

2. **Base de Datos**:

    ```bash
    bin/rails db:prepare
    ```

3. **Ejecución**:
    Para iniciar todos los servicios (Web, CSS Watcher y Job Worker):

    ```bash
    bin/dev
    ```

## 🧪 Pruebas

Para ejecutar la suite de pruebas (incluyendo la nueva limpieza automática):

```bash
bin/rails test
```

## 🔑 Configuración de LinkedIn (Importante)

Para que la búsqueda en LinkedIn funcione con tu cuenta y obtenga mejores resultados:

1. Cierra todas las sesiones de Rails o terminales relacionadas con LinkedIn.
2. Ejecuta el script de autenticación:

    ```bash
    ./venv/bin/python get_linkedin_cookies.py
    ```

3. Se abrirá una ventana de Chrome. Inicia sesión manualmente.
4. Una vez veas tu perfil, cierra la ventana o regresa a la terminal.
5. El archivo `linkedin_cookies.json` se habrá creado y la aplicación lo usará automáticamente en segundo plano.

## 📋 Tareas Programadas (Recurring Tasks)

La aplicación utiliza `Solid Queue` para tareas recurrentes. Configurado en `config/recurring.yml`:

* `weekly_job_cleanup`: Elimina vacantes de > 7 días. Ejecución: 3:00 AM diario.
