from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from airflow.operators.bash import BashOperator  # type: ignore
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule  # type: ignore
from CoinMarketCap.scripts.load_staging import load_staging
from airflow.models import Variable  #type: ignore
import os

# 1. Cấu hình thông số mặc định cho các Task
default_args = {
    'owner': 'qtrung',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # BẮT BUỘC phải có start_date để Airflow xác định mốc thời gian bắt đầu chạy pipeline
    'start_date': datetime(2026, 5, 1), 
}

# 2. Khai báo cấu trúc DAG (Chạy tự động vào lúc 0h00 mỗi ngày)
with DAG(
    dag_id='pipeline_elt_coin_v1',
    default_args=default_args,
    description='Hệ thống chạy ELT tự động cho CoinMarketCap Data Warehouse',
    schedule='0 0 * * *', # Chạy định kỳ lúc 00:00 hàng ngày
    catchup=False,                  # Không chạy bù các ngày quá khứ kể từ start_date
) as dag:
    task_load_staging=PythonOperator(
        task_id='load_staging',
        python_callable=load_staging
    )
    project_dir = "/opt/airflow/projects/CoinMarketCap/database/dbt_for_coin"
    profile_dir= "/opt/airflow/projects/CoinMarketCap/config"
    run_dbt_build = BashOperator(
        task_id='execute_dbt_build',
        bash_command=f"cd {project_dir} && dbt build --profiles-dir {profile_dir}",
        env={
            #Giữ lại toàn bộ biến môi trường mặc định của hệ thống 
            **os.environ,
            # Lấy giá trị từ Airflow Variable và gắn vào biến môi trường DB_PASSWORD cho dbt đọc
            "DB_PASSWORD": "{{ var.value.DB_PASSWORD }}"
    }
    )
    task_load_staging>>run_dbt_build # type: ignore
