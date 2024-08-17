# edimcaDispatch
# Dispatch Track API Integration Script

Este repositorio contiene un script de Python diseñado para integrarse con la API de Dispatch Track, extrayendo datos de rutas y despachos para su procesamiento y almacenamiento en una base de datos SQL Server.

## Descripción General

El script realiza lo siguiente:
- Realiza solicitudes HTTP a la API de Dispatch Track para obtener datos de rutas.
- Procesa los datos recibidos y los estructura para inserción en SQL Server.
- Inserta los datos procesados en una tabla específica de SQL Server.

## Requisitos

El script requiere Python 3.6+ y algunas librerías externas para su correcta ejecución. Asegúrate de que tu sistema cumpla con estos requisitos básicos.

## Instalación de Librerías

Antes de ejecutar el script, necesitas instalar las siguientes librerías:

- `requests`: Para realizar solicitudes HTTP.
- `pandas`: Para el manejo de datos y transformaciones.
- `pyodbc`: Para interactuar con la base de datos SQL Server.

Puedes instalar estas librerías utilizando pip con el siguiente comando:

```bash
pip install requests pandas pyodbc

python C:/path/to/dispatchTrack.py
```



## Configuración del Job en SQL Server Agent

Para automatizar la ejecución del script de integración con la API de Dispatch Track utilizando SQL Server Agent, sigue estos pasos:

### Crear un Nuevo Job

1. **Abrir SQL Server Management Studio (SSMS)** y conectarse a la instancia de SQL Server donde deseas configurar el job.
2. Navega hasta **SQL Server Agent** en el explorador de objetos y expande el nodo.
3. Haz clic derecho en **Jobs** y selecciona **New Job**.

### Configurar Propiedades del Job

4. En la ventana de diálogo **New Job**, asigna un nombre descriptivo al job en el campo **Name**.
5. Opcionalmente, proporciona una descripción en el campo **Description**.

### Agregar Steps al Job

6. Ve a la pestaña **Steps** y haz clic en **New** para crear un nuevo step.
7. Asigna un nombre al step en **Step name**.
8. En **Type**, selecciona **Operating system (CmdExec)**.
9. En el campo **Command**, introduce el comando para ejecutar el script. Por ejemplo:
   ```cmd
   python "C:\path\to\your\script.py"

