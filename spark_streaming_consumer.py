from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, TimestampType, LongType

# Definir el esquema (molde) de los datos JSON que llegan de Kafka
schema = StructType()

# Crear la SparkSession (punto de entrada)
spark = SparkSession.builder \
  .appName("KafkaSparkStreaming") \
  .getOrCreate()

# Reducir el nivel de log para una salida más limpia
spark.sparkContext.setLogLevel("WARN")

# Crear un DataFrame de streaming que lee desde el topic de Kafka
df = spark.readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "sensor_data") \
  .load()

# 1. Parsear los datos de binario a JSON estructurado
# Convertimos el valor de binario a string y luego a columnas usando el esquema
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
            .select("data.*")

# 2. Convertir el timestamp de Unix Long a Spark Timestamp
# Usamos col("timestamp") y lo casteamos a TimestampType
parsed_df_with_timestamp = parsed_df.withColumn("timestamp_col", col("timestamp").cast(TimestampType()))

# 3. Calcular estadísticas agregadas sobre ventanas de 1 minuto
windowed_stats = parsed_df_with_timestamp \
  .groupBy(
        # Agrupamos por ventana de 1 minuto (Tumbling Window)
        window(col("timestamp_col"), "1 minute"), 
        "sensor_id"
    ) \
  .agg(

round(avg("temperature"), 2).alias("avg_temp"),
        round(avg("humidity"), 2).alias("avg_humidity")
    ) \
   .orderBy(col("window").asc(), col("sensor_id").asc())

# 4. Definir el "sink" (destino): Imprimir los resultados en la consola
query = windowed_stats.writeStream \
  .outputMode("update") \
  .format("console") \
  .option("truncate", "false") \
  .start()

# Esperar a que la consulta termine (se ejecuta indefinidamente)
query.awaitTermination()
