#!/usr/bin/env python
"""Extract only horse purchasing events from kafka and write them to hdfs
"""

# libraries
import json
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

# set up schema for the horse purchase events
def purchase_horse_event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- timestamp: string (nullable = true)
    |-- speed: string (nullable = true)
    |-- size: string (nullable = true)
    |-- quantity: string (nullable = true)
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("speed", StringType(), True),
        StructField("size", StringType(), True),
        StructField("quantity", StringType(), True),
    ])


@udf('boolean')
def is_horse_purchase(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase_horse':
        return True
    return False


def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()

    horse_purchases = raw_events \
        .filter(is_horse_purchase(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          purchase_horse_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')
    
    sink = horse_purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_horse_purchases") \
        .option("path", "/tmp/horse_purchases") \
        .trigger(processingTime="10 seconds") \
        .start()  
        
    sink.awaitTermination()


if __name__ == "__main__":
    main()
