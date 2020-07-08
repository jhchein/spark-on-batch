import argparse
import logging

import config
from pyspark.sql import SparkSession

logger = logging.getLogger("analyticslogger")
logger.setLevel("DEBUG")

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def get_azure_spark_connection(storage_account_name, storage_account_key):
    spark = (
        SparkSession.builder.config(
            "spark.jars.packages", "org.apache.hadoop:hadoop-azure:2.7.3"
        )
        .config(
            "spark.hadoop.fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem"
        )
        .config(
            "spark.hadoop.fs.azure.account.key."
            + storage_account_name
            + ".blob.core.windows.net",
            storage_account_key,
        )
        .appName("AzureSparkDemo")
        .getOrCreate()
    )

    (
        spark.sparkContext._jsc.hadoopConfiguration().set(
            "fs.wasbs.impl", "org.apache.hadoop.fs.azure.NativeAzureFileSystem"
        )
    )
    return spark


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        help="input file to parse",
        type=str,
        default="wasbs://titanic@sparkonbatch.blob.core.windows.net/train.csv",
    )
    parser.add_argument("--pclass", type=int, default=1)
    parser.add_argument(
        "--output",
        help="result file to write",
        type=str,
        default="wasbs://titanic@sparkonbatch.blob.core.windows.net/output_1.parquet",
    )
    args = parser.parse_args()
    logger.info(f"file: {args.file}")
    logger.info(f"pclass: {args.pclass}")
    logger.info(f"output: {args.output}")

    logger.info("establishing spark connection")
    spark = get_azure_spark_connection(
        config.STORAGE_ACCOUNT_NAME, config.STORAGE_ACCOUNT_KEY
    )

    logger.info("reading dataframe")
    df = (
        spark.read.option("header", "true")
        .option("delimiter", ",")
        .option("inferSchema", "true")
        .csv(args.file)
    )

    logger.info("registering dataframe")
    df.registerTempTable("titanic")

    query = f"""
        select Sex, Pclass, avg(Survived) as survival_rate, avg(Age) as avg_age, avg(SibSp) as avg_sibsp, avg(Parch) as avg_parch, avg(Fare) as avg_fare
        from titanic 
        where Pclass={args.pclass}
        group by Sex, Pclass
        """
    logger.info(f"query: {query}")
    result = spark.sql(query)

    logger.info(f"head:\n {result.head(2)}")

    logger.info("writing output")
    result.repartition(1).write.mode("overwrite").parquet(args.output)
    logger.info("done")
