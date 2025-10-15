# 🧭 Guía de instalación de Kubernetes en Ubuntu (WSL2)

> ✅ Objetivo: tener un clúster local de Kubernetes funcional dentro de WSL usando **Minikube** y **kubectl**, sin depender de Docker Desktop.

---

## 📋 1️⃣ Requisitos previos

Asegúrate de tener:

- Windows 10/11 con **WSL2 habilitado**  
  (verifica con `wsl -l -v`)
- Distribución **Ubuntu 22.04 o 24.04**
- Al menos **4 GB RAM** y **2 CPU**
- **Virtualización activada** en BIOS
- **Internet estable**

---

## ⚙️ 2️⃣ Actualiza el sistema

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget apt-transport-https ca-certificates gnupg lsb-release
````

---

## 🐳 3️⃣ Instala un motor de contenedores

Minikube necesita un *driver* para crear el clúster.
La forma más liviana en WSL es usar **Docker Engine nativo de Linux**:

```bash
sudo apt install -y docker.io
sudo usermod -aG docker $USER
```

Luego **reinicia tu sesión WSL** (sal y vuelve a entrar) y prueba:

```bash
docker ps
```

Debe mostrar sin errores.

---

## ☸️ 4️⃣ Instala Minikube

Descarga e instala el binario oficial:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Verifica:

```bash
minikube version
```

---

## 🧩 5️⃣ Instala kubectl (cliente de Kubernetes)

### Paso 1: Instala dependencias

```bash
sudo apt install -y curl apt-transport-https ca-certificates gnupg
```

### Paso 2: Agrega la clave GPG oficial

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | \
sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
```

### Paso 3: Agrega el repositorio oficial

```bash
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /" | \
sudo tee /etc/apt/sources.list.d/kubernetes.list
```

### Paso 4: Instala kubectl

```bash
sudo apt update
sudo apt install -y kubectl
```

### Verifica la instalación

```bash
kubectl version --client
```

---

## 🚀 6️⃣ Inicia Kubernetes con Minikube

Crea tu clúster local:

```bash
minikube start --driver=docker
```

> 💡 Esto descargará una imagen de control plane de Kubernetes y la ejecutará dentro de Docker en WSL.

Comprueba que todo está bien:

```bash
minikube status
kubectl get nodes
```

Deberías ver algo como:

```bash
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   2m    v1.31.x
```

---

## 🛠️ 7️⃣ Configuración opcional (recomendada)

### Hacer que `kubectl` use siempre Minikube por defecto

```bash
kubectl config use-context minikube
```

### Exponer el dashboard de Kubernetes

```bash
minikube dashboard --url
```

---

## 🧼 8️⃣ Comandos útiles

| Acción                 | Comando               |
| :--------------------- | :-------------------- |
| Ver estado del clúster | `minikube status`     |
| Detener el clúster     | `minikube stop`       |
| Eliminar todo          | `minikube delete`     |
| Listar pods            | `kubectl get pods -A` |
| Ver logs del clúster   | `minikube logs`       |

---

## ⚠️ 9️⃣ Consejos finales

- Si ves errores de permisos con Docker, asegúrate de que tu usuario esté en el grupo `docker` y reinicia WSL.
- Si WSL se queda sin recursos, aumenta RAM o CPUs con:
  `%USERPROFILE%\.wslconfig`
- Puedes cambiar de driver con `--driver=none` (modo nativo sin Docker, usa namespaces de Linux).

---

## ✅ Resultado final

Tu entorno Kubernetes local dentro de WSL debería quedar operativo:

```bash
$ kubectl get nodes
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   3m    v1.31.0
```

Listo para desplegar pods, servicios y practicar con YAML o Helm 🎯
