#import spark
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType
from databricks.sdk import WorkspaceClient

w = WorkspaceClient(host=input('Databricks Workspace URL: '), token=input('Token: '))

schema = StructType([
  StructField("month", StringType(), True),
  StructField("day", IntegerType(), True),
  StructField("time", StringType(), True),
  StructField("host", StringType(), True),
  StructField("process", StringType(), True),
  StructField("log_date", TimestampType(), True),
  StructField("log_time", StringType(), True),
  StructField("message", StringType(), True)
])

#month,day,time,host,process,log_date,log_time,message

df = spark.read.format("csv").option("header", True).schema(schema).load("/data/wardcs_parsed.csv")

# Create the table if it does not exist. Otherwise, replace the existing table.
df.writeTo("main.default.people_10m").createOrReplace()

# If you know the table does not already exist, you can call this instead:
# df.saveAsTable("main.default.people_10m")