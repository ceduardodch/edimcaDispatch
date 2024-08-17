import requests
import pandas as pd
import pyodbc
from datetime import datetime


# Configura la URL de la API y el token de autorización
url = 'https://edimca.dispatchtrack.com/api/external/v1/routes'
token = '21ecd590686f34549c9c4e7c5ea9ce13923fe26f8623d3ad053ade5ace96e24c'

# Configura la conexión a la base de datos SQL Server
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=172.16.150.44;'
    r'DATABASE=STAGE;'
    r'UID=USRDWH;'
    r'PWD=USR05DWH17;'
)

# Función para hacer la solicitud HTTP a la API
def get_http_response(url, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'X-AUTH-TOKEN': token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Lanza una excepción si la solicitud falla
    return response.json()

# Función para convertir datos a formato seguro

def safe_convert(value, dtype):
    if dtype == 'float':
        try:
            return float(value) if value not in [None, ''] else None
        except ValueError:
            return None
    elif dtype == 'int':
        try:
            return int(value) if value not in [None, ''] else None
        except ValueError:
            return None
    elif dtype == 'str':
        return str(value) if value is not None else ''
    elif dtype == 'datetime':
        try:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S') if value not in [None, ''] else None
        except ValueError:
            return None
    elif dtype == 'bool':
        return bool(value) if value is not None else None
    else:
        return value
# Función principal
def main():
    # Hacer la solicitud a la API
    data = get_http_response(url, token)

    # Mostrar el JSON recibido (Impresión en consola)
    print("JSON Response:")
    print(data)

    # Procesar los datos
    routes = data.get('response', {}).get('routes', [])
    dispatches_data = []

    for route in routes:
        for dispatch in route.get('dispatches', []):
            dispatches_data.append({
                'route_id': safe_convert(route.get('id'), 'str'),
                'dispatch_date': safe_convert(route.get('dispatch_date'), 'str'),
                'truck_identifier': safe_convert(route.get('truck', {}).get('identifier', ''), 'str'),
                'vehicle_type': safe_convert(route.get('truck', {}).get('vehicle_type', ''), 'str'),
                'group_name': safe_convert(route.get('truck', {}).get('groups', [{}])[0].get('name', ''), 'str') if route.get('truck', {}).get('groups') else '',
                'group_value': safe_convert(route.get('truck', {}).get('groups', [{}])[0].get('value', ''), 'str') if route.get('truck', {}).get('groups') else '',
                'driver_identifier': safe_convert(route.get('driver_identifier', ''), 'str'),
                'driver_name': safe_convert(route.get('driver_name', ''), 'str'),
                'driver_app_version': safe_convert(route.get('driver_app_version', ''), 'str'),
                'start_time': safe_convert(route.get('start_time', ''), 'str'),
                'end_time': safe_convert(route.get('end_time', ''), 'str'),
                'started_at': safe_convert(route.get('started_at', ''), 'str'),
                'dispatch_id': safe_convert(dispatch.get('identifier', ''), 'str'),
                'contact_name': safe_convert(dispatch.get('contact_name', ''), 'str'),
                'contact_address': safe_convert(dispatch.get('contact_address', ''), 'str'),
                'contact_phone': safe_convert(dispatch.get('contact_phone', ''), 'str'),
                'contact_id': safe_convert(dispatch.get('contact_id', ''), 'str'),
                'contact_email': safe_convert(dispatch.get('contact_email', ''), 'str'),
                'latitude': safe_convert(dispatch.get('latitude', ''), 'str'),
                'longitude': safe_convert(dispatch.get('longitude', ''), 'str'),
                'status': safe_convert(dispatch.get('status', ''), 'str'),
                'status_id': safe_convert(dispatch.get('status_id', 0), 'int'),
                'substatus': safe_convert(dispatch.get('substatus',''), 'int'),
                'substatus_code': safe_convert(dispatch.get('substatus_code', ''), 'str'),
                'is_trunk': safe_convert(dispatch.get('is_trunk', ''), 'str'),
                'is_pickup': safe_convert(dispatch.get('is_pickup', ''), 'str'),
                'arrived_at': safe_convert(dispatch.get('arrived_at', ''), 'datetime'),
                'estimated_at': safe_convert(dispatch.get('estimated_at', ''), 'datetime'),
                'min_delivery_time': safe_convert(dispatch.get('min_delivery_time', ''), 'datetime'),
                'max_delivery_time': safe_convert(dispatch.get('max_delivery_time', ''), 'datetime'),
                'delivery_time': safe_convert(dispatch.get('delivery_time', ''), 'str'),
                'beecode': safe_convert(dispatch.get('beecode', ''), 'str'),
                'numero_factura': next((tag.get('Numero de Factura') for tag in dispatch.get('tags', []) if 'Numero de Factura' in tag), ''),
                'tiene_cheque': next((tag.get('Tiene Cheque') for tag in dispatch.get('tags', []) if 'Tiene Cheque' in tag), ''),
                'numero_de_orden': next((tag.get('Numero de orden') for tag in dispatch.get('tags', []) if 'Numero de orden' in tag), ''),
                'tipo_orden': next((tag.get('Tipo orden') for tag in dispatch.get('tags', []) if 'Tipo orden' in tag), ''),
                'numero_linea': next((tag.get('Numero linea') for tag in dispatch.get('tags', []) if 'Numero linea' in tag), ''),
                'mails_centro_distribucion': next((tag.get('Mails Centros de Distribucion') for tag in dispatch.get('tags', []) if 'Mails Centros de Distribucion' in tag), ''),
                'mails_sucursales': next((tag.get('Mails Sucursales') for tag in dispatch.get('tags', []) if 'Mails Sucursales' in tag), ''),
            })

    # Convertir los datos en un DataFrame de pandas
    df = pd.DataFrame(dispatches_data)

    # Conectar a la base de datos SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Insertar los datos en la tabla de la base de datos
    for index, row in df.iterrows():
        try:
            cursor.execute("""
            INSERT INTO DispatchRoutebk (
                route_id, dispatch_date, truck_identifier, vehicle_type, group_name, group_value, driver_identifier, driver_name, driver_app_version, start_time,
                end_time, started_at, dispatch_id, contact_name, contact_address, contact_phone, contact_id, contact_email, latitude, longitude,
                status, status_id, substatus, substatus_code, is_trunk, is_pickup, arrived_at, estimated_at, min_delivery_time, max_delivery_time,
                delivery_time, beecode, numero_factura, tiene_cheque, numero_de_orden, tipo_orden, numero_linea, mails_centro_distribucion, mails_sucursales
                ) 
                VALUES (    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?)""", tuple(row))
            conn.commit()
        except Exception as e:
            print(f"Error inserting row {index}: {e}")

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Guardar los datos en un archivo CSV (opcional)
    df.to_csv('dispatch_data.csv', index=False)

    # Imprimir los primeros registros (opcional)
    print(df.head())

if __name__ == "__main__":
    main()