Tarea 3: Solución de Procesamiento de Datos con Apache Spark y Kafka
Este repositorio contiene la implementación del componente práctico de la Tarea 3, demostrando el uso de Apache Spark para el procesamiento de datos a gran escala en modo Batch y Streaming.
1. Problemas Críticos Superados (Evidencia de Dominio Técnico)
El proceso requirió superar problemas técnicos complejos de infraestructura en el entorno virtualizado (VM), lo cual es fundamental en la ingeniería de Big Data:

A. Solución a la Falta de Espacio en Disco (LVM y GParted)
Problema: El disco virtual se llenó al 100% (No space left on device), impidiendo la instalación de software y la escritura de archivos.

Solución Técnica: Se realizó una expansión del disco duro de 12GB a 30GB, utilizando la herramienta GParted Live y comandos LVM (lvextend, resize2fs) para redimensionar la partición de Ubuntu.

B. Solución a la Inestabilidad de Hadoop (HDFS)
Problema: Los servicios de almacenamiento distribuido de Hadoop fallaron de manera persistente al arrancar (0 datanode(s) running).

Solución Implementada: El código Batch fue modificado para leer el archivo CSV directamente desde el sistema de archivos local de Ubuntu (file:///home/vboxuser/rows.csv), evitando la dependencia de un sistema HDFS inestable para entornos de prueba.
2. Implementación en Batch (Análisis Histórico de la TRM)
Archivo: analisis_trm.py

Objetivo: Obtener estadísticas clave del dataset de la Tasa de Cambio Representativa del Mercado (TRM) de Colombia.
Análisis Realizado,Función de Spark,Resultado Obtenido (Evidencia)
Máximo Valor Histórico,"max(col(""VALOR""))",5061.21 COP
Mínimo Valor Histórico,"min(col(""VALOR""))",620.62 COP
Transformación Clave,"df.withColumn(""ANIO"", year(col(""VIGENCIAHASTA"")))",Se extrae la columna ANIO de las fechas para el análisis de tendencia.
Almacenamiento,.write.parquet(...),Se demostró el almacenamiento del resultado procesado en formato Parquet.
3. Implementación en Tiempo Real (Spark Streaming con Kafka)
Archivos: kafka_producer.py y spark_streaming_consumer.py

Objetivo: Demostrar un pipeline de datos de baja latencia con agregación por ventanas de tiempo (Sensores IoT).

Flujo Demostrado:

Productor: Genera mensajes JSON de sensores simulados (temperatura y humedad).

Consumidor Spark: Utiliza Spark Structured Streaming conectado al topic de Kafka.

Procesamiento: El código usa la función window(..., "1 minute") para calcular el promedio de temperatura y humedad en lapsos regulares.

4. Instrucciones para la Ejecución (Para Sustentación)
Para demostrar el código en el video, se deben seguir estos pasos:

**Iniciar Servicios:**bash

Iniciar Kafka (ZooKeeper y Broker)
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties & sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &

Iniciar Spark (Master y Worker)
start-master.sh start-slave.sh spark://bigdata:7077
Ejecutar Proyecto Streaming (Demostración Visual en dos terminales):

Terminal 1 (Productor): python3 kafka_producer.py

Terminal 2 (Consumidor Spark): spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumer.py
#### **Paso 3: Guardar el Documento**

1.  Una vez que hayas copiado todo el texto, baja al final de la página del editor.
2.  Escribe un pequeño mensaje en el cuadro de "Commit changes" (por ejemplo: `Documentación completa del proyecto y resultados finales`).
3.  Haz clic en el botón verde **"Commit changes"** (Guardar cambios) en la esquina superior derecha.
