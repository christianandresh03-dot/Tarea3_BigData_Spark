# analisis_trm.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, avg, count, max, min, round

# 1. Iniciar la sesión de Spark
# El nombre de la aplicación es Tarea3
spark = SparkSession.builder.appName('Tarea3-TRM').getOrCreate()

# 2. Definir la ruta del archivo.csv en el disco local de la VM
# Usamos 'file:///' para leer directamente del sistema de archivos de Ubuntu
file_path = 'file:///home/vboxuser/rows.csv'

# 3. Cargar el dataset (Asumiendo que las columnas son VALOR, UNIDAD, VIGENCIADESDE, VIGENCIAHASTA)
# Option header: true -> Usa la primera fila como nombres de columna
# Option inferSchema: true -> Spark adivina el tipo de dato
df = spark.read.format('csv').option('header', 'true').option('inferSchema', 'true').load(file_path)

# 4. Limpieza y Transformación (Quitamos filas nulas y creamos una columna anio)
df_limpio = df.na.drop()
df_transformado = df_limpio.withColumn("ANIO", year(col("VIGENCIAHASTA")))

# 5. Análisis Exploratorio de Datos (EDA)
print("--- Esquema de los Datos ---")
df_transformado.printSchema()

# Pregunta 1: Tasa de cambio promedio por año
print("\n--- TRM Promedio por Año ---")
trm_por_anio = df_transformado.groupBy("ANIO") \
   .agg(round(avg(col("VALOR")), 2).alias("TRM_Promedio")) \
   .orderBy(col("ANIO").desc())
trm_por_anio.show(5)

# Pregunta 2: Máximo y Mínimo valor histórico de la TRM
print("\n--- Valores Extremos de la TRM (Máximo y Mínimo) ---")
extremos = df_transformado.agg(
    max(col("VALOR")).alias("Maximo_Valor"),
    min(col("VALOR")).alias("Minimo_Valor")
)
extremos.show()

# 6. Almacenar los resultados (En este caso, en el disco local, ya que HDFS está inestable)
print("\n--- Guardando el resultado procesado en disco local ---")
df_transformado.write.mode("overwrite").parquet("/home/vboxuser/resultados_trm.parquet")

# Detener la sesión
spark.stop()
