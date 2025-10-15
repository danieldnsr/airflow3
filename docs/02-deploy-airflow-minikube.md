# Desplegar Airflow 3 en Minikube (WSL2)

Guía paso a paso para desplegar Apache Airflow 3 con PostgreSQL en Minikube.

---

## 1. Preparar el entorno

```bash
# Iniciar Minikube con recursos suficientes
minikube start --cpus=4 --memory=8192 --driver=docker

# Verificar que funciona
kubectl get nodes
```

---

## 2. Crear el namespace

```bash
kubectl create namespace airflow
```

---

## 3. Desplegar PostgreSQL

Crear archivo `postgres-deployment.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: airflow
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: airflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_USER
          value: airflow
        - name: POSTGRES_PASSWORD
          value: airflowpassword
        - name: POSTGRES_DB
          value: airflow
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: airflow
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

Desplegar:

```bash
kubectl apply -f postgres-deployment.yaml

# Esperar a que esté listo
kubectl wait --for=condition=ready pod -l app=postgres -n airflow --timeout=300s
```

---

## 4. Configurar Airflow

Crear archivo `values-minimal.yaml`:

```yaml
postgresql:
  enabled: false

data:
  metadataConnection:
    user: airflow
    pass: airflowpassword
    protocol: postgresql
    host: postgres
    port: 5432
    db: airflow
    sslmode: disable

redis:
  enabled: true
  persistence:
    enabled: false

executor: "CeleryExecutor"

images:
  airflow:
    repository: apache/airflow
    tag: "3.0.2"

fernetKey: "REEMPLAZAR_CON_TU_CLAVE"

webserver:
  replicas: 1
  service:
    type: NodePort
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

scheduler:
  resources:
    requests:
      cpu: 100m
      memory: 256Mi

workers:
  resources:
    requests:
      cpu: 100m
      memory: 256Mi

triggerer:
  resources:
    requests:
      cpu: 100m
      memory: 128Mi

logs:
  persistence:
    enabled: false
```

Generar clave Fernet:

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copiar el resultado y reemplazar `REEMPLAZAR_CON_TU_CLAVE` en el archivo.

---

## 5. Instalar Airflow con Helm

```bash
# Agregar repositorio
helm repo add apache-airflow https://airflow.apache.org
helm repo update

# Instalar
helm install airflow apache-airflow/airflow \
  --namespace airflow \
  -f values-minimal.yaml \
  --timeout 10m

# Ver el progreso
kubectl get pods -n airflow -w
```

---

## 6. Acceder a la UI

```bash
# Hacer port-forward
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
```

Abrir en el navegador: <http://localhost:8080>

**Credenciales:**

- Usuario: `admin`
- Contraseña: `admin`

---

## Solución de problemas

### Pods en ImagePullBackOff

Verificar que las imágenes sean accesibles:

```bash
docker pull postgres:16-alpine
docker pull apache/airflow:3.0.2
```

### Ver logs de un pod

```bash
kubectl logs -n airflow <nombre-del-pod>
```

### Reiniciar despliegue

```bash
helm uninstall airflow -n airflow
kubectl delete pvc --all -n airflow
# Volver a instalar
```

---

**¡Listo!** Airflow 3 corriendo en Minikube.
