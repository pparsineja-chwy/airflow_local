
import logging
from datetime import datetime, timedelta
import json
import os
import boto3
from pytz import timezone

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow import Dataset
from airflow.models.param import Param
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DAG_ID = os.path.basename(__file__).replace(".py", "")

SNOWFLAKE_CONN_ID = "worker_pricing_analytics_airflow_svc"

AWS_ENVIRONMENT = 'dev'
AWS_ACCOUNT_NUMBER = '748090408311'

AWS_SEGMENTED_ACCOUNT_NAME = 'worker_pricing_analytics_dev'

ACCOUNT_VPC = "worker_pricing_analytics-vpc-dev"

AWS_SECRET = "/chewy/dev/us-east-1/worker_pricing_analytics/airflow/connections/worker_pricing_analytics_airflow_svc"

# bucket for data processing, features and etc.
# s3://dev-use1-worker-pricing-analytics-data
S3_AIRFLOW_BUCKET =   f"dev-use1-worker-pricing-analytics-repository"
S3_DATA_BUCKET =      f"dev-use1-worker-pricing-analytics-data"
S3_CATALOGE_BUCKET =  f"dev-use1-worker-pricing-analytics-catalog"
S3_SAGEMAKER_BUCKET = f"dev-use1-worker-pricing-analytics-sagemaker"

GLUE_ROLE = "dev-use1-worker_pricing_analytics-glue"
GLUE_ROLE_ARN = f"arn:aws:iam::{AWS_ACCOUNT_NUMBER}:role/{GLUE_ROLE}"
GLUE_DATABASE = "worker_pricing_analytics_catalog"
GLUE_WORKER_TYPE = "G.1X"
GLUE_CONNECTION = "dev-use1-worker-pricing-analytics-connection"
S3_GLUE_ASSEST_BUCKET = f"aws-glue-assets-{AWS_ACCOUNT_NUMBER}-us-east-1"
S3_GLUE_ASSEST_BUCKET_ARN = f"arn:aws:s3:::aws-glue-assets-{AWS_ACCOUNT_NUMBER}-us-east-1"

SNOWFLAKE_ROLE_NAME = 'PRICING_ANALYTICS_MSS_DEVELOPER_DEV'
SNOWFLAKE_DATABASE_NAME = 'EDLDB_DEV'
SNOWFLAKE_SCHEMA_NAME = "PRICING_ANALYTICS_MSS_SANDBOX"
SNOWFLAKE_INTEGRATION_NAME = 'DEV_CHEWY_BI_WORKER_PRICING_ANALYTICS_MSS_INT'
SNOWFLAKE_WAREHOUSE_NAME = 'PRICING_ANALYTICS_MSS_WH'

DEFAULT_ARGS = {
    "owner": "Pricing Analytics and Data Science",
    "depends_on_past": False,
    "retries": 0,
    "email": ["pparsineja@chewy.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "snowflake_conn_id":SNOWFLAKE_CONN_ID
}

with DAG(
        dag_id=DAG_ID,
        description="Snowflake Connection Test",
        default_args=DEFAULT_ARGS,
        start_date=days_ago(1),
        schedule_interval=None,
        tags=["Snowflake", "Connection", "Test"]
) as dag:
    begin = DummyOperator(
        task_id="begin"
    )

    end = DummyOperator(
        task_id="end"
    )
    
    snowflake_task = SnowflakeOperator(
            task_id=f"snowflake_task",
            sql="select count(1) from edldb.chewybi.products;",
            params={
                "role": SNOWFLAKE_ROLE_NAME,
                "warehouse": SNOWFLAKE_WAREHOUSE_NAME,
                "db_name": SNOWFLAKE_DATABASE_NAME,
                "sandbox_name": SNOWFLAKE_SCHEMA_NAME,
                "s3_bucket_name":f"s3://{S3_DATA_BUCKET}",
                "s3_integration": SNOWFLAKE_INTEGRATION_NAME,
            }
    )

    begin >> snowflake_task >> end