#!/usr/bin/env python
"""Extract only guild events from kafka and write them to hdfs
"""

# libraries
import json
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

# set up schema for the guild events
def guild_event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- timestamp: string (nullable = true)
    |-- action: string (nullable = true)
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("action", StringType(), True)
    ])


@udf('boolean')
def is_guild(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'guild':
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

    guild_actions = raw_events \
        .filter(is_guild(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          guild_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')
    
    sink = guild_actions \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_guild_actions") \
        .option("path", "/tmp/guild_actions") \
        .trigger(processingTime="10 seconds") \
        .start()  
        
    sink.awaitTermination()
    

if __name__ == "__main__":
    main()
