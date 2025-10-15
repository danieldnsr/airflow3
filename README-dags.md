# DAGs de Prueba - Hola Mundo con Docker y Kubernetes

Este proyecto contiene dos DAGs de Apache Airflow para probar la integración con Docker y Kubernetes.

## 📁 Estructura del Proyecto

```
airflow3/
├── dags/
│   ├── hello_world_docker_dag.py    # DAG con DockerOperator
│   └── hello_world_k8s_dag.py       # DAG con KubernetesPodOperator
├── docs/
├── values-minimal.yaml              # Configuración de Airflow para Kubernetes
└── postgres-deployment.yaml        # Deployment de PostgreSQL
```

## 🚀 DAGs Incluidos

### 1. `hello_world_docker` (DockerOperator)

**Archivo:** `dags/hello_world_docker_dag.py`

Este DAG ejecuta contenedores Docker directamente y contiene 3 tareas:

1. **docker_hola_mundo**: Saludo básico con Alpine Linux
2. **docker_system_info**: Información del sistema 
3. **docker_python_hello**: Prueba con Python

**Características:**
- Usa imágenes ligeras (`alpine:latest`, `python:3.9-alpine`)
- Auto-eliminación de contenedores (`auto_remove=True`)
- Ejecución manual (`schedule_interval=None`)

### 2. `hello_world_kubernetes` (KubernetesPodOperator)

**Archivo:** `dags/hello_world_k8s_dag.py`

Este DAG ejecuta pods de Kubernetes y contiene 4 tareas:

1. **k8s_hola_mundo**: Saludo básico en pod Alpine
2. **k8s_cluster_info**: Información del cluster de Kubernetes
3. **k8s_ubuntu_tools**: Prueba con Ubuntu y herramientas
4. **k8s_python_advanced**: Script avanzado de Python

**Características:**
- Configuración de recursos CPU/memoria
- Auto-eliminación de pods después de la ejecución
- Logs detallados de cada pod
- Namespace configurable (por defecto: `default`)

## 🛠️ Configuración y Despliegue

### Requisitos Previos

1. **Minikube** ejecutándose
2. **Airflow** desplegado en Kubernetes usando Helm
3. **Docker** disponible en los nodos de Kubernetes
4. **PostgreSQL** ejecutándose (usando `postgres-deployment.yaml`)

### Pasos para Desplegar

1. **Verificar que Airflow esté ejecutándose:**
   ```bash
   kubectl get pods -l app.kubernetes.io/name=airflow
   ```

2. **Copiar los DAGs al volumen persistente de Airflow:**
   
   Si usas volúmenes persistentes, copia la carpeta `dags/` al volumen correspondiente.
   
   Si usas GitSync (recomendado), haz commit y push de los DAGs:
   ```bash
   git add dags/
   git commit -m "Agregar DAGs de prueba Hola Mundo"
   git push origin main
   ```

3. **Verificar que los DAGs aparezcan en la UI de Airflow:**
   - Accede a la UI de Airflow
   - Ve a la pestaña "DAGs"
   - Deberías ver `hello_world_docker` y `hello_world_kubernetes`

### Acceder a la UI de Airflow

Si configuraste el servicio como `NodePort`:

```bash
# Obtener la URL del servicio
minikube service airflow-webserver --url

# O hacer port-forwarding
kubectl port-forward svc/airflow-webserver 8080:8080
# Luego acceder a http://localhost:8080
```

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin`

## 🧪 Cómo Probar los DAGs

### 1. Probar el DAG de Docker

1. En la UI de Airflow, busca `hello_world_docker`
2. Activa el DAG (toggle ON)
3. Haz clic en "Trigger DAG" para ejecutarlo manualmente
4. Ve a "Graph View" para monitorear el progreso
5. Haz clic en cada tarea para ver los logs

### 2. Probar el DAG de Kubernetes

1. En la UI de Airflow, busca `hello_world_kubernetes`
2. Activa el DAG (toggle ON)
3. Haz clic en "Trigger DAG"
4. Monitorea en "Graph View"
5. Los pods se ejecutarán en paralelo/secuencia según las dependencias

### 3. Verificar desde la Terminal

```bash
# Ver pods de Airflow
kubectl get pods -l app.kubernetes.io/name=airflow

# Ver logs de un pod específico (mientras se ejecuta)
kubectl logs <pod-name> -f

# Ver todos los pods (incluyendo los temporales de las tareas)
kubectl get pods --all-namespaces
```

## 🔧 Troubleshooting

### Error: "Docker not found"
- Verifica que Docker esté instalado en los nodos de Kubernetes
- Asegúrate de que el socket de Docker (`/var/run/docker.sock`) esté montado

### Error: "Image pull failed"
- Verifica conectividad a internet desde el cluster
- Las imágenes (`alpine`, `python`, `ubuntu`) se descargan automáticamente

### Error: "Pod creation timeout"
- Aumenta `startup_timeout_seconds` en el KubernetesPodOperator
- Verifica recursos disponibles: `kubectl describe nodes`

### Los DAGs no aparecen en la UI
- Verifica que los archivos estén en la ruta correcta de DAGs
- Revisa logs del scheduler: `kubectl logs deployment/airflow-scheduler`
- Verifica sintaxis de Python: `python -m py_compile dags/hello_world_*.py`

## 📊 Logs y Monitoreo

### Ver logs de tareas Docker:
- En la UI de Airflow: Task Instance → View Log
- Los logs mostrarán la salida de los comandos Docker

### Ver logs de tareas Kubernetes:
- En la UI de Airflow: Task Instance → View Log  
- También puedes usar: `kubectl logs <pod-name>` mientras el pod existe

### Monitorear recursos:
```bash
# CPU y memoria de los pods
kubectl top pods

# Eventos del cluster
kubectl get events --sort-by=.metadata.createdAt

# Estado de los nodos
kubectl get nodes
kubectl describe nodes
```

## 🎯 Próximos Pasos

Una vez que estos DAGs funcionen correctamente, puedes:

1. **Agregar más complejidad:** Tareas con dependencias de datos
2. **Integrar con almacenamiento:** Usar PersistentVolumes
3. **Agregar monitoring:** Prometheus + Grafana
4. **Configurar alertas:** Slack, email, etc.
5. **Usar secretos:** Para credenciales sensibles
6. **Implementar CI/CD:** Para despliegue automatizado de DAGs

## 📝 Notas Adicionales

- Los DAGs están configurados para ejecución manual (`schedule_interval=None`)
- Los recursos están limitados para funcionar en Minikube
- Los pods se eliminan automáticamente después de la ejecución
- Los contenedores Docker también se auto-eliminan

¡Disfruta probando tu setup de Airflow + Kubernetes! 🎉