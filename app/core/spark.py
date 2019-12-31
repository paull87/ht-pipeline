import os
from pyspark.context import SparkContext, SparkConf


def get_spark_context(workers="*", driver_memory=None, executor_memory=None):
    """
    This function sets up a local Spark context, configured for use with SQL Server and AWS S3.
    """

    # we need some libraries (jars) to connect to SQL Server and S3, so define this config
    jar_dir = r"C:\Jars"

    files = os.listdir(jar_dir)

    jars = [f for f in files if f.lower().endswith(".jar")]

    extra_class_path = ";".join([os.path.join(jar_dir, j) for j in jars])

    # setup spark context
    conf = SparkConf().setMaster(f"local[{workers}]") \
        .set("spark.driver.extraClassPath", extra_class_path) \
        .set("spark.executor.heartbeatInterval", "60s")

    if driver_memory:
        conf.set("spark.driver.memory", driver_memory)

    if executor_memory:
        conf.set("spark.executor.memory", executor_memory)

    spark_context = SparkContext(conf=conf)

    # we need to configure our s3 endpoint because our buckets are in London
    spark_context.setSystemProperty("com.amazonaws.services.s3.enableV4", "true")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.eu-west-2.amazonaws.com")

    return spark_context
