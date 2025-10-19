# Pod Initialization with `nslookup` in Kubernetes

This example demonstrates how to use an **initContainer** in Kubernetes to ensure a dependent service is available **before** the main application container starts.

## ⚙️ Overview

The pod includes:

- **`app-container`** → Main application  
- **`initContainer`** → Waits for a service (`myservice`) to become resolvable via DNS

## 🧠 How It Works

```bash
until nslookup myservice.default.svc.cluster.local; do 
  echo "Waiting for service to be up"; 
  sleep 2; 
done
````

This loop keeps checking if `myservice` exists in the cluster DNS.
Once it resolves, the initContainer finishes, and the main app container starts.

## Flow Diagram

```text
+------------------------+
|   Init Container       |
|------------------------|
| while ! nslookup ...   |
|   sleep 2              |
| done                   |
+-----------+------------+
            |
            v
+------------------------+
|   Main Container       |
|------------------------|
|  Application Starts ✅  |
+------------------------+
```

---

## 📡 Why Use This Pattern?

✅ Ensures dependent services are available before startup  
✅ Prevents connection failures during initialization  
✅ Works well for microservice dependencies (e.g., API ↔ Database)  

✨ **This setup helps maintain startup order and stability in Kubernetes deployments.**
