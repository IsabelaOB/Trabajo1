import csv
import json
import os
import time
import uuid
import boto3

print("Obteniendo endpoint de AWS IoT Core...")

# 2. Obtener endpoint automáticamente
iot_client = boto3.client("iot", region_name="us-east-1")
endpoint_response = iot_client.describe_endpoint(endpointType="iot:Data-ATS")
endpoint_url = f"https://{endpoint_response['endpointAddress']}"

print(f"Endpoint detectado: {endpoint_url}")

data_client = boto3.client("iot-data",
                           region_name="us-east-1",
                           endpoint_url=endpoint_url)

# 3. Leer los 10.000 datos del CSV
RUTA_CSV = "consumo_sintetico_subestaciones.csv"
if not os.path.exists(RUTA_CSV):
    RUTA_CSV = "labs/consumo_sintetico_subestaciones.csv"

print(f"Cargando los datos desde {RUTA_CSV}...")

with open(RUTA_CSV, mode="r", encoding="utf-8-sig") as f:
    lector = list(csv.DictReader(f))

# Tomamos los primeros 10.000 eventos para completar la inyección requerida
eventos_a_enviar = lector[:10000]
total = len(eventos_a_enviar)

print(
    f"Iniciando inyección de {total} eventos de subestaciones hacia AWS IoT...")

for i, fila in enumerate(eventos_a_enviar, start=1):
    payload = {
        "event_id": str(uuid.uuid4()),
        "medidor": fila.get("Medidor"),
        "fecha": fila.get("Fecha"),
        "hora": int(fila.get("Hora del día", 0)),
        "kwh": float(fila.get("Energía activa (kWh)", 0.0)),
        "timestamp_envio": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    data_client.publish(topic="iot/eventos", qos=0, payload=json.dumps(payload))

    if i % 1000 == 0:
        print(f"Progreso: {i} / {total} eventos inyectados exitosamente...")

print("¡Inyección completada con éxito al 100%!")
