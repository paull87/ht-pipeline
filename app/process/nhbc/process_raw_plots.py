import datetime
from dateutil.relativedelta import relativedelta
from pyspark.sql import SQLContext, Window
from pyspark.sql import functions as func
from app.core.spark import get_spark_context
from app.settings.envs import NHBC_BUCKET
from app.core.logging import logger


SPARK_CONTEXT = get_spark_context("2")
SQL_CONTEXT = SQLContext(SPARK_CONTEXT)

RAW_S3_URL = f's3a://{NHBC_BUCKET}/raw/{{month}}/{{file}}'
PLOTS = 'Plots.csv'
PROJECTS = 'Projects.csv'
TRANSFORMED_S3_URL = f's3a://{NHBC_BUCKET}/transformed/plots/month={{month}}/'

DF_OPTIONS = {
    "header": True,
    "sep": "|",
    "escape": '"'
}


def load_raw_plots(month):
    url = RAW_S3_URL.format(month=month, file=PLOTS)
    logger.info(f'Loading {url}')
    df = SQL_CONTEXT.read \
        .option("header", True) \
        .option("sep", "|") \
        .csv(url)

    return df


def load_processed_plots(month):
    month_format = f'{month[:4]}-{month[-2:]}'
    url = TRANSFORMED_S3_URL.format(month_format)
    logger.info(f'Loading {url}')
    df = SQL_CONTEXT.read.options(DF_OPTIONS).csv(url)

    # sometimes there are duplicate PLOT_IDs so discard the duplicates here
    window = Window.partitionBy(df['PLOT_ID']).orderBy(df.columns)
    df = df.select("*", func.rank().over(window).alias("row_number")).filter("row_number = 1").drop("row_number")

    return df


def load_raw_projects(month):
    url = RAW_S3_URL.format(month=month, file=PROJECTS)
    logger.info(f'Loading {url}')
    df = SQL_CONTEXT.read.option("header", True).option("sep", "|").csv(url)
    return df


def get_plots_with_projects(plots_df, projects_df):
    logger.info(f'Combining plots and project data frames')
    project_reference_df = projects_df \
        .select("Project Reference") \
        .distinct() \
        .withColumnRenamed("Project Reference", "PROJECT_REFERENCE")

    df = plots_df.join(project_reference_df, "PROJECT_REFERENCE", "inner")

    return df


def write_processed_plots_to_s3(month, plots_df):
    month_format = f'{month[:4]}-{month[-2:]}'
    url = TRANSFORMED_S3_URL.format(month_format)
    logger.info(f'Writing to S3 {url}')
    plots_df.repartition(1).write.options(DF_OPTIONS).csv(path=url, mode="overwrite")


def process_initial_data(month):
    plots_df = load_raw_plots(month)
    projects_df = load_raw_projects(month)
    processed_plots_df = get_plots_with_projects(plots_df, projects_df)
    write_processed_plots_to_s3(month, processed_plots_df)


def get_reference_month(month):
    month_date = datetime.datetime.strptime(month, '%Y%m')
    reference_month = month_date - relativedelta(months=1)
    return reference_month.strftime('%Y%m')


def process_cumulative_data(month, reference_month=None):
    if reference_month is None:
        reference_month = get_reference_month(month)

    # load the new raw data and the previous processed file
    new_df = load_raw_plots(month)
    reference_df = load_processed_plots(reference_month)

    # use PLOT_ID to identify records which we want to roll forward
    ids_df = reference_df.select("PLOT_ID").subtract(new_df.select("PLOT_ID"))
    missing_plots_df = reference_df.join(ids_df, "PLOT_ID", "inner")
    plots_df = new_df.union(missing_plots_df.select(new_df.columns))

    # filter to plots with matching project
    projects_df = load_raw_projects(month)
    plots_df = get_plots_with_projects(plots_df, projects_df)

    # save results
    write_processed_plots_to_s3(month, plots_df)
