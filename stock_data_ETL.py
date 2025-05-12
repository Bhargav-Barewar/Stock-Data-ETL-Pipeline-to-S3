from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import requests
import boto3
from airflow.models import Variable
from airflow.utils.dates import days_ago
import os


API_KEY = Variable.get("api_key")
AWS_ACCESS_KEY = Variable.get("aws_access_key")
AWS_SECRET_KEY = Variable.get("aws_secret_key")
S3_BUCKET = Variable.get("s3_bucket")

default_args = {
    'start_date': datetime(2025, 1, 1)
}
dag = DAG(
    'stock_etl_to_s3',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

def extract():
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?timeseries=200&apikey={API_KEY}'
    data = requests.get(url).json()
    df = pd.DataFrame(data['historical'])
    df.to_csv('/tmp/stock_raw.csv', index=False)

def transform():
    df = pd.read_csv('/tmp/stock_raw.csv')
    df['50_SMA'] = df['close'].rolling(window=50).mean()
    df['200_SMA'] = df['close'].rolling(window=200).mean()
    df.to_csv('/tmp/stock_transformed.csv', index=False)

def load(**context):
    execution_date = context['ds']
    s3_file = f"AAPL_{execution_date}.csv"
    s3 = boto3.client(
        's3',
        aws_access_key_id = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY
    )
    s3.upload_file('/tmp/stock_transformed.csv', S3_BUCKET, s3_file)
    print(f"file is successfully uploaded to s3://{S3_BUCKET}/{s3_file}")
    # Clean up temporary files
    os.remove('/tmp/stock_raw.csv')
    os.remove('/tmp/stock_transformed.csv')

E = PythonOperator(task_id='extract', python_callable=extract, dag=dag)
T = PythonOperator(task_id='transform', python_callable=transform, dag=dag)
L = PythonOperator(task_id='load_to_S3', python_callable=load, provide_context=True, dag=dag)

E >> T >> L