from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys
import os

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from my_functions.my_python_function import my_python_function, get_user, get_playlists, get_accessToken, get_artists, get_tracks, load_s3

# Define your DAG configuration
default_args = {
    'owner': 'saad',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'my_test_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Adjust the schedule as needed
    catchup=False,
    max_active_runs=1,
)

# Create a PythonOperator that runs your Python function
my_task = PythonOperator(
    task_id='start',
    python_callable=my_python_function,
    dag=dag,
)

get_accessToken_task = PythonOperator(
    task_id='get_accessToken_task',
    python_callable=get_accessToken,
    dag=dag,
)
# Create PythonOperator tasks for get_user() and get_playlists()
get_user_task = PythonOperator(
    task_id='get_user_task',
    python_callable=get_user,
    dag=dag,
)

get_user_artists = PythonOperator(
    task_id='get_user_artists',
    python_callable=get_artists,
    dag=dag,
)

get_playlists_task = PythonOperator(
    task_id='get_playlists_task',
    python_callable=get_playlists,
    dag=dag,
)
get_tracks = PythonOperator(
    task_id='get_tracks',
    python_callable=get_tracks,
    dag=dag,
)

load_s3 = PythonOperator(
    task_id='load_s3',
    python_callable=load_s3,
    dag=dag,
)

# Set the task dependencies
my_task >> get_accessToken_task >> get_user_task >> get_user_artists >> get_playlists_task >> get_tracks >> load_s3
#my_task >> get_accessToken_task >> get_playlists_task
if __name__ == "__main__":
    dag.cli()