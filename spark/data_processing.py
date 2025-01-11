from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from minio import Minio
import os

spark = SparkSession.builder \
    .appName("ECommercePipeline") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.postgresql:postgresql:42.5.4") \
    .getOrCreate()

minio_client = Minio("minio:9000", "minioadmin", "minioadmin", secure=False)

schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("action", StringType()),
    StructField("timestamp", LongType())
])

def process_batch(batch_df, epoch_id):
    try:
        print(f"Received batch {epoch_id} with {batch_df.count()} records")
        batch_df.show()  # Show incoming Kafka data
        
        local_csv_path = f"/tmp/product_catalog_{epoch_id}.csv"
        minio_client.fget_object("data", "product_catalog.csv", local_csv_path)
        
        product_catalog = spark.read.csv(local_csv_path, header=True) \
            .withColumn("user_id", col("user_id").cast("int"))
        print("Product catalog data:")
        product_catalog.show()
        
        enriched_df = batch_df.join(product_catalog, "user_id", "left") \
            .withColumn("product_id", col("product_id").cast("int"))  # Cast product_id to integer

        print("Enriched data:")
        enriched_df.show()
        
        print(f"Writing {enriched_df.count()} records to PostgreSQL")
        enriched_df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/ecommerce") \
            .option("dbtable", "user_actions") \
            .option("user", "admin") \
            .option("password", "password") \
            .mode("append") \
            .save()
            
    except Exception as e:
        print(f"Error in batch {epoch_id}: {str(e)}")
        raise e
    finally:
        if os.path.exists(local_csv_path):
            os.remove(local_csv_path)

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "user_actions") \
    .load() \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# Add this before the writeStream to check raw Kafka messages
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "user_actions") \
    .load()

def print_raw(df, epoch_id):
    print("Raw Kafka messages:")
    df.select(col("value").cast("string")).show(truncate=False)

raw_df.writeStream.foreachBatch(print_raw).start()

query = df.writeStream \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()