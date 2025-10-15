"""
DAG de prueba - Hola Mundo con KubernetesPodOperator
===================================================

Este DAG ejecuta pods de Kubernetes que corren contenedores Docker
para probar la integración completa de Airflow + Kubernetes + Docker.

Autor: Daniel
Fecha: Octubre 2025
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

# Configuración por defecto para el DAG
default_args = {
    'owner': 'daniel',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

# Definición del DAG
dag = DAG(
    'hello_world_kubernetes',
    default_args=default_args,
    description='DAG de prueba con Kubernetes que ejecuta Hola Mundo en pods',
    schedule_interval=None,  # Ejecutar manualmente
    catchup=False,
    tags=['kubernetes', 'k8s', 'hola-mundo', 'prueba'],
)

# Task 1: Hola Mundo básico en Kubernetes
k8s_hello_task = KubernetesPodOperator(
    task_id='k8s_hola_mundo',
    name='airflow-hello-mundo-pod',
    namespace='default',
    image='alpine:latest',
    cmds=['sh', '-c'],
    arguments=['echo "¡Hola Mundo desde Kubernetes! ⚙️🐳" && echo "Pod ejecutándose en: $(hostname)" && echo "Fecha: $(date)"'],
    dag=dag,
    is_delete_operator_pod=True,
    get_logs=True,
    startup_timeout_seconds=120,
)

# Task 2: Información detallada del cluster
k8s_cluster_info_task = KubernetesPodOperator(
    task_id='k8s_cluster_info',
    name='airflow-cluster-info-pod',
    namespace='default',
    image='alpine:latest',
    cmds=['sh', '-c'],
    arguments=[
        'echo "=== INFORMACIÓN DEL CLUSTER ===" && '
        'echo "Hostname del pod: $(hostname)" && '
        'echo "Namespace: ${KUBERNETES_NAMESPACE:-default}" && '
        'echo "Usuario actual: $(whoami)" && '
        'echo "Sistema operativo: $(uname -a)" && '
        'echo "Memoria disponible:" && cat /proc/meminfo | grep MemTotal && '
        'echo "CPU info:" && cat /proc/cpuinfo | grep "model name" | head -1 && '
        'echo "Variables de entorno de Kubernetes:" && env | grep KUBERNETES | head -5'
    ],
    dag=dag,
    is_delete_operator_pod=True,
    get_logs=True,
    startup_timeout_seconds=120,
    # Configuración de recursos
    container_resources=k8s.V1ResourceRequirements(
        requests={'cpu': '100m', 'memory': '128Mi'},
        limits={'cpu': '500m', 'memory': '256Mi'}
    ),
)

# Task 3: Prueba con Ubuntu y herramientas adicionales
k8s_ubuntu_task = KubernetesPodOperator(
    task_id='k8s_ubuntu_tools',
    name='airflow-ubuntu-tools-pod',
    namespace='default',
    image='ubuntu:20.04',
    cmds=['bash', '-c'],
    arguments=[
        'echo "¡Hola desde Ubuntu en Kubernetes! 🐧" && '
        'echo "Actualizando paquetes..." && '
        'apt-get update -qq && apt-get install -y curl wget -qq && '
        'echo "Probando conectividad:" && '
        'curl -s -I https://www.google.com | head -1 && '
        'echo "Información del contenedor:" && '
        'cat /etc/os-release | grep PRETTY_NAME && '
        'echo "Directorio actual: $(pwd)" && '
        'echo "Archivos en /:" && ls -la / | head -10'
    ],
    dag=dag,
    is_delete_operator_pod=True,
    get_logs=True,
    startup_timeout_seconds=180,  # Más tiempo para Ubuntu
    container_resources=k8s.V1ResourceRequirements(
        requests={'cpu': '200m', 'memory': '256Mi'},
        limits={'cpu': '500m', 'memory': '512Mi'}
    ),
)

# Task 4: Prueba con Python en Kubernetes
k8s_python_task = KubernetesPodOperator(
    task_id='k8s_python_advanced',
    name='airflow-python-advanced-pod',
    namespace='default',
    image='python:3.9-slim',
    cmds=['python', '-c'],
    arguments=['''
import sys
import os
import platform
import datetime

print("🐍 ¡Hola Mundo desde Python en Kubernetes!")
print(f"Versión de Python: {sys.version}")
print(f"Plataforma: {platform.platform()}")
print(f"Arquitectura: {platform.architecture()}")
print(f"Nombre del host: {platform.node()}")
print(f"Fecha y hora: {datetime.datetime.now()}")
print(f"Variables de entorno de Kubernetes:")
for key, value in os.environ.items():
    if 'KUBERNETES' in key:
        print(f"  {key}: {value}")

# Pequeña demostración de procesamiento
print("\\n🧮 Pequeña demostración de cálculo:")
numeros = list(range(1, 11))
suma = sum(numeros)
print(f"Suma de números del 1 al 10: {suma}")
print(f"Números pares: {[n for n in numeros if n % 2 == 0]}")
print("\\n✅ Prueba completada exitosamente!")
    '''],
    dag=dag,
    is_delete_operator_pod=True,
    get_logs=True,
    startup_timeout_seconds=120,
    container_resources=k8s.V1ResourceRequirements(
        requests={'cpu': '100m', 'memory': '128Mi'},
        limits={'cpu': '300m', 'memory': '256Mi'}
    ),
)

# Definir dependencias: ejecutar en paralelo los primeros dos, luego los otros dos
[k8s_hello_task, k8s_cluster_info_task] >> k8s_ubuntu_task >> k8s_python_task