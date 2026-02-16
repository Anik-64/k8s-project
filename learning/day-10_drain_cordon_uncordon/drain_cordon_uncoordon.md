# **Kubernetes Node Maintenance: cordon vs drain vs uncordon**

Kubernetes provides **three core commands** to safely manage nodes during maintenance, upgrades, or failures:

```
cordon   → stop scheduling new pods
drain    → evict existing pods safely
uncordon → allow scheduling again
```

---

## 1️⃣ `kubectl cordon`

### What it does

Marks a node as **unschedulable**.

```bash
kubectl cordon node1
```

### Behavior

* ❌ No new pods will be scheduled
* ✅ Existing pods keep running
* ❌ No pod eviction happens

### When to use

* Before maintenance
* Before draining
* When you want to “freeze” a node

### Example

```bash
kubectl cordon worker-1
```

This is a **safe, non-destructive action**.

---

## 2️⃣ `kubectl drain`

### What it does

Safely **evicts pods** from a node and prepares it for maintenance.

```bash
kubectl drain node1
```

### What happens internally

1. Node is cordoned automatically
2. Kubernetes tries to evict pods
3. Pods are recreated on other nodes **if possible**
4. Safety checks are enforced

---

## 3️⃣ Pod behavior during `drain`

### ✅ Controller-managed pods (SAFE)

| Pod Type                | Drain Behavior | Recreated? |
| ----------------------- | -------------- | ---------- |
| Deployment / ReplicaSet | Evicted        | ✅ Yes      |
| StatefulSet             | Evicted        | ✅ Yes      |
| Job / CronJob           | Evicted        | ✅ Yes      |

These pods are **self-healing**.

---

### ⚠ DaemonSet pods (SPECIAL)

* Ignored by default
* Node-specific workloads (logs, CNI, monitoring)

```bash
kubectl drain node1 --ignore-daemonsets
```

---

### ❌ Standalone pods (DANGEROUS)

Pods **not managed by any controller**:

```yaml
kind: Pod
metadata:
  name: standalone-pod
```

#### Default behavior

```bash
kubectl drain node1
```

❌ Drain **fails**
Kubernetes protects you.

#### Forced behavior

```bash
kubectl drain node1 --force
```

⚠ **Pod is deleted permanently**

❗ No ReplicaSet → no recreation → **data loss**

---

## 4️⃣ Why forced drain deletes pods forever

Because **Pods are not self-healing objects**.

| Object      | Self-Healing |
| ----------- | ------------ |
| Pod         | ❌ No         |
| ReplicaSet  | ✅ Yes        |
| Deployment  | ✅ Yes        |
| StatefulSet | ✅ Yes        |

Kubernetes only knows **what controllers know**.

---

## 5️⃣ `kubectl uncordon`

### What it does

Allows scheduling again on the node.

```bash
kubectl uncordon node1
```

### Behavior

* ✅ New pods can be scheduled
* ❌ Old pods are NOT automatically moved back

Pods stay where the scheduler placed them.

---

## 6️⃣ Full lifecycle (REAL WORLD FLOW)

```bash
kubectl cordon node1
kubectl drain node1 --ignore-daemonsets
# do maintenance
kubectl uncordon node1
```

This is how **production upgrades** are done.

---

## 7️⃣ Summary Table (VERY IMPORTANT)

| Command       | Schedules New Pods | Evicts Existing Pods | Risk    |
| ------------- | ------------------ | -------------------- | ------- |
| cordon        | ❌ No               | ❌ No                 | None    |
| drain         | ❌ No               | ✅ Yes                | Medium  |
| drain --force | ❌ No               | ✅ Yes                | 🔥 High |
| uncordon      | ✅ Yes              | ❌ No                 | None    |

---

## 8️⃣ Best Practices (Production)

✅ Always deploy apps using controllers
❌ Avoid standalone pods
✅ Use `cordon` before `drain`
❌ Avoid `--force` unless absolutely necessary
✅ Check workloads before draining:

```bash
kubectl get pods -o wide
```

---

**Cordon**

> Stops new pods from scheduling but keeps existing pods running.

**Drain**

> Safely evicts controller-managed pods and prepares the node for maintenance.

**Force Drain**

> Deletes standalone pods permanently because no controller exists to recreate them.

**Uncordon**

> Allows scheduling again but does not move pods back automatically.
