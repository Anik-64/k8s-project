
## 🔹 **What is a Secret?**

A **Secret** in Kubernetes is an object that stores **sensitive information** such as:

* Passwords
* API keys
* Tokens
* Certificates
* Credentials

Secrets allow you to **avoid hardcoding sensitive data** inside your Pod or Deployment YAML files.

# 🔹 Why do we use Secrets?

Using Secrets provides:

### ✔ Security

Sensitive data is stored separately, not inside Pod YAML files.

### ✔ Easy Update

Updating a secret updates the environment variables inside pods (with restart or rollout).

### ✔ Flexible Usage

You can use secrets as:

* Environment variables
* Files mounted into pods
* Image pull credentials

# 🔹 Types of Secrets

| Secret Type         | Description                               |
| ------------------- | ----------------------------------------- |
| **Opaque**          | Default type (key-value pairs)            |
| **docker-registry** | Used for pulling private container images |
| **tls**             | Stores TLS cert + key                     |
| **basic-auth**      | Username/password auth                    |
| **ssh-auth**        | SSH private keys                          |

# 🔹 How to Create a Secret (Imperative Command)

### **1️⃣ Create using literals**

```sh
kubectl create secret generic env-secret \
  --from-literal=USER=anik \
  --from-literal=PASS=1234
```

### **2️⃣ Create from a file**

```sh
kubectl create secret generic file-secret --from-file=secret.txt
```

### **3️⃣ Generate YAML without creating**

```sh
kubectl create secret generic env-secret \
  --from-literal=USER=anik \
  --from-literal=PASS=1234 \
  --dry-run=client -o yaml > env-secret.yaml
```

# 🔹 How to Use Secrets Inside Pods

### **1️⃣ Load all keys using envFrom**

```yaml
envFrom:
  - secretRef:
      name: env-secret
```

Environment variables inside container:

```
$USER → anik
$PASS → 1234
```

### **2️⃣ Load specific keys using env**

```yaml
env:
  - name: USER
    valueFrom:
      secretKeyRef:
        name: env-secret
        key: USER
```

### **3️⃣ Mount secret as file**

```yaml
volumeMounts:
  - name: secrets
    mountPath: "/etc/secret-data"

volumes:
  - name: secrets
    secret:
      secretName: env-secret
```

# 🔹 How to View Secrets

### Base64 encoded:

```sh
kubectl get secret env-secret -o yaml
```

### Decode value:

```sh
echo "YW5paw==" | base64 --decode
```

# 🔹 Advantages of Secrets

### ✔ Security

Sensitive data is not exposed inside YAML files.

### ✔ Lightweight

Stored in etcd, encoded in Base64.

### ✔ Flexible usage

Works as env variables or mounted files.

### ✔ Easy updates

You can rotate passwords without modifying deployments.

# 🔹 Disadvantages of Secrets

### ❌ Base64 is NOT encryption

It’s only obfuscation.
Actual encryption depends on **etcd encryption**, which must be enabled.

### ❌ Anyone with access to the cluster role can read secrets

RBAC must be properly configured.

### ❌ Mounted secrets require pod restart to update inside running containers

# 🔹 Best Practices

* ✔ Enable **Encryption at Rest** for etcd
* ✔ Limit access to Secrets using **RBAC**
* ✔ Never store plain passwords in Git
* ✔ Use `--dry-run` to generate secret YAML without storing sensitive data
* ✔ Rotate secrets regularly
