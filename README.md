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





