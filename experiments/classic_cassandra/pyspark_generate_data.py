from pyspark.sql import SparkSession
import random
import uuid
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, FloatType
from tqdm import tqdm
from dotenv import load_dotenv
from cassandra.cluster import Cluster

# Load environment variables
load_dotenv()

# Initialize Cassandra connection
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Create keyspace and table if not exists
session.execute(
    """CREATE KEYSPACE IF NOT EXISTS embeddings
    WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };
    """
)

session.execute("USE embeddings;")

session.execute(
    """
    CREATE TABLE IF NOT EXISTS embeddings.video_embeddings (
      video_id uuid,
      frame int,
      embedding list<float>,
      PRIMARY KEY (video_id, frame)
    )
    WITH CLUSTERING ORDER BY (frame DESC);
    """
)

session.execute_async(
    """CREATE INDEX IF NOT EXISTS ann_index
      ON embeddings.video_embeddings(embedding) USING 'sai';"""
)

# Initialize Spark session with the Cassandra connector package
spark = SparkSession.builder \
    .appName("CassandraDataIngestion") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0") \
    .getOrCreate()

# UDF to generate random embeddings
def generate_embedding(length):
    return [random.random() for _ in range(length)]

embed_udf = udf(lambda length: generate_embedding(length), ArrayType(FloatType()))

# Generate a Spark DataFrame with the video embeddings
def generate_video_embeddings(num_videos, video_length, embedding_length):
    video_id = str(uuid.uuid4())  # Generate a unique video_id

    # Create schema for DataFrame
    schema = StructType([
        StructField("video_id", StringType(), True),
        StructField("frame", IntegerType(), True),
        StructField("embedding", ArrayType(FloatType()), True)
    ])

    # Generate data
    data = []
    for frame in range(video_length):
        embedding = generate_embedding(embedding_length)
        data.append((video_id, frame, embedding))

    return spark.createDataFrame(data, schema)

# Function to insert data into Cassandra
def insert_data_to_cassandra(dataframe):
    dataframe.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode('append') \
        .options(table="video_embeddings", keyspace="embeddings") \
        .save()

# Generate and insert data
if __name__ == "__main__":
    num_videos = 109
    video_length = 27000
    embedding_length = 1000

    for _ in tqdm(range(num_videos), total=num_videos):
        df = generate_video_embeddings(1, video_length, embedding_length)
        insert_data_to_cassandra(df)

    print(f"{num_videos * video_length} entries have been successfully inserted into the database.")