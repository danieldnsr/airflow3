"""
DAG de prueba - Hola Mundo con DockerOperator
===============================================

Este DAG ejecuta un contenedor Docker simple que imprime "Hola Mundo" 
para probar la integración de Airflow con Docker en Kubernetes.

Autor: Daniel
Fecha: Octubre 2025
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

# Configuración por defecto para el DAG
default_args = {
    'owner': 'daniel',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definición del DAG
dag = DAG(
    'hello_world_docker',
    default_args=default_args,
    description='DAG de prueba con Docker que ejecuta Hola Mundo',
    schedule=None,  # Ejecutar manualmente (Airflow 3.x syntax)
    catchup=False,
    tags=['docker', 'hola-mundo', 'prueba'],
)

# Task 1: Hola Mundo básico
hello_task = DockerOperator(
    task_id='docker_hola_mundo',
    image='alpine:latest',
    command='echo "¡Hola Mundo desde Docker! 🐳"',
    dag=dag,
    auto_remove='success',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
)

# Task 2: Información del sistema
system_info_task = DockerOperator(
    task_id='docker_system_info',
    image='alpine:latest',
    command='sh -c "echo \'=== Información del Sistema ===\' && uname -a && echo \'=== Fecha y Hora ===\' && date && echo \'=== Contenido del directorio ===\' && ls -la /"',
    dag=dag,
    auto_remove='success',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
)

# Task 3: Prueba con Python
python_task = DockerOperator(
    task_id='docker_python_hello',
    image='python:3.9-alpine',
    command='python -c "print(\'¡Hola desde Python en Docker! 🐍\'); import sys; print(f\'Versión de Python: {sys.version}\')"',
    dag=dag,
    auto_remove='success',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
)

# Definir dependencias: las tareas se ejecutan en secuencia
hello_task >> system_info_task >> python_task