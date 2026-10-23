# Proyecto Integrador - Big Data (Trabajo 1)

---

## 📌 Descripción del Proyecto

Este proyecto implementa una arquitectura end-to-end para el procesamiento masivo de datos de consumo eléctrico, dividida en dos bloques principales:

1. **Parte A (Procesamiento Batch - Capas Medallion):** Pipeline analítico en AWS Athena utilizando el formato **Apache Iceberg** sobre Amazon S3 para procesar y auditar más de 1.1 millones de registros.
2. **Parte B (Procesamiento Near Real-Time - Streaming IoT):** Tubería serverless desacoplada para ingestar y almacenar eventos de sensores en tiempo real mediante **AWS IoT Core**, **AWS SQS**, **AWS Lambda** y **Amazon DynamoDB**.

---

## 🏗️ Arquitectura del Sistema

### Parte A: Capas Medallion (AWS Athena + Apache Iceberg + S3)

* **Bronce (Raw):** Ingesta del dataset original (`~1.138.800` registros) en Amazon S3 como tabla externa en Athena con tipado en texto (`STRING`).
* **Tabla de Hallazgos:** Consulta de auditoría para cuantificar registros nulos y valores inválidos ($\le 0 \text{ kWh}$).
* **Plata (Clean & Enriched):** Separación en dos tablas Apache Iceberg (Parquet):
  * `consumo_plata_validos`: Registros limpios con casteo explícito de tipos (`DATE`, `INT`, `DOUBLE`).
  * `consumo_plata_rechazados`: Registros descartados etiquetados con la causa raíz.
  * **Verificación de Calidad:** $\text{Filas Bronce} = \text{Filas Válidas} + \text{Filas Rechazadas}$.
* **Oro (Business Aggregations):** Tabla Iceberg pre-agregada que responde al consumo total, promedio y máximo por subestación, año y mes.

### Parte B: Streaming de Eventos IoT

* **Inyección (`inyectar.py`):** Script simulador en Python que transmite $10.000$ eventos con la estructura del proyecto (`medidor`, `kwh`, `fecha`, `hora`, `timestamp_envio`).
* **Ingesta y Desacoplamiento:** Regla de **AWS IoT Core** que intercepta mensajes MQTT y los encola en **AWS SQS** para actuar como buffer de absorción.
* **Procesamiento y Persistencia:** **AWS Lambda** consume la cola por lotes de forma asíncrona y realiza la persistencia en **Amazon DynamoDB** (Partition Key: `event_id`).

---

## 🛠️ Tecnologías Utilizadas

* **Cloud Provider:** Amazon Web Services (AWS) - Configuración 100% manual (0% IaC).
* **Storage & Data Lake:** Amazon S3, Amazon DynamoDB.
* **Analytics & Query Engine:** AWS Athena, Apache Iceberg (Parquet).
* **Streaming & Serverless:** AWS IoT Core, AWS SQS, AWS Lambda.
* **Lenguajes & Entorno:** Python 3.x, SQL, Docker (`.devcontainer`), VS Code.

---

## 🚀 Ejecución del Código

### 1. Variables de Entorno

Configurar las credenciales temporales de AWS en el archivo `.env`:

```env
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_SESSION_TOKEN=tu_session_token
AWS_DEFAULT_REGION=us-east-1
