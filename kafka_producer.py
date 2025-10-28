import time
import json
import random
from kafka import KafkaProducer

# Funcion que genera una lectura simulada de temperatura y humedad
def generate_sensor_data():
    return {
        "sensor_id": random.randint(1, 10),
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "timestamp": int(time.time())
    }
# Inicializar el productor de Kafka, conectandose al broker local
# El value_serializer es crucial para convertir el diccionario de Python a bytes (JSON)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("Iniciando Productor. Enviando datos de sensores a Kafka...")
while True:
    sensor_data = generate_sensor_data()
    # Enviar los datos al topic 'sensor_data'
    producer.send('sensor_data', value=sensor_data)
    print(f"Enviado: {sensor_data}")
    time.sleep(1) # Enviar un mensaje cada segundo
