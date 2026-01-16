# Part 1 — Is `type` always `Container` in LimitRange?

LimitRange supports **3 types**:

| Type                    | What it controls                    |
| ----------------------- | ----------------------------------- |
| `Container`             | Individual containers (most common) |
| `Pod`                   | The entire pod (sum of containers)  |
| `PersistentVolumeClaim` | Storage size limits                 |

---

## Examples of other types

### Pod-level limits

```yaml
type: Pod
max:
  cpu: "2"
  memory: "2Gi"
```

### PVC limits

```yaml
type: PersistentVolumeClaim
min:
  storage: 1Gi
max:
  storage: 10Gi
```

---

# Part 2 — Deep explanation of your LimitRange fields

Your config:

```yaml
type: Container
default:
  cpu: "500m"
  memory: "256Mi"
defaultRequest:
  cpu: "200m"
  memory: "128Mi"
max:
  cpu: "1"
  memory: "512Mi"
min:
  cpu: "100m"
  memory: "64Mi"
```

Let’s explain each one with real behavior:

---

## 1️⃣ `default`

> Applied when user does NOT specify `resources.limits`

Example Pod without limits:

```yaml
resources: {}
```

Kubernetes will auto-add:

```yaml
limits:
  cpu: 500m
  memory: 256Mi
```

✔ Prevents unlimited containers
✔ Protects the cluster

---

## 2️⃣ `defaultRequest`

> Applied when user does NOT specify `resources.requests`

Scheduler uses requests to place pods on nodes.

Kubernetes adds:

```yaml
requests:
  cpu: 200m
  memory: 128Mi
```

✔ Ensures proper scheduling
✔ Prevents overbooking nodes

---

## 3️⃣ `max`

> Upper limit allowed per container

If someone deploys:

```yaml
limits:
  cpu: 2
```

❌ Pod will be rejected:

```
exceeds max cpu of 1
```

✔ Prevents runaway containers

---

## 4️⃣ `min`

> Minimum required resource

If someone deploys:

```yaml
requests:
  cpu: 50m
```

❌ Pod will be rejected:

```
less than min cpu of 100m
```

✔ Prevents under-provisioning
✔ Ensures stable performance

---

# Visual behavior of LimitRange

| Case                   | Result           |
| ---------------------- | ---------------- |
| No resources specified | defaults applied |
| Too high resources     | rejected         |
| Too low resources      | rejected         |
| Valid range            | allowed          |

---

# Part 3 — Explanation of ResourceQuota

Your quota:

```yaml
hard:
  pods: "20"
  requests.cpu: "4"
  requests.memory: "8Gi"
  limits.cpu: "8"
  limits.memory: "16Gi"
```

This controls **total namespace usage**.

---

## 1️⃣ `pods: "20"`

Max number of pods in namespace = 20

If 21st pod created:

❌ rejected

---

## 2️⃣ `requests.cpu: "4"`

Sum of ALL pod requests CPU ≤ 4 cores

Example:

| Pod  | CPU Request |
| ---- | ----------- |
| pod1 | 500m        |
| pod2 | 1           |
| pod3 | 1           |
| pod4 | 1           |
| pod5 | 700m        |

Total = 4.2 ❌ rejected

---

## 3️⃣ `requests.memory: "8Gi"`

Total requested memory ≤ 8Gi

Used by scheduler capacity planning

---

## 4️⃣ `limits.cpu: "8"`

Total CPU limits of all pods ≤ 8 cores

Even if requests fit, limits cannot exceed this

---

## 5️⃣ `limits.memory: "16Gi"`

Total memory limits ≤ 16Gi

---

# LimitRange vs ResourceQuota (together)

| Feature               | LimitRange | ResourceQuota |
| --------------------- | ---------- | ------------- |
| Per container control | ✔          | ❌             |
| Per namespace total   | ❌          | ✔             |
| Default values        | ✔          | ❌             |
| Enforce min/max       | ✔          | ❌             |
| Cap total resources   | ❌          | ✔             |

---

# Real-world behavior example

Developer deploys:

```yaml
resources:
  requests:
    cpu: 3
    memory: 6Gi
  limits:
    cpu: 4
    memory: 10Gi
```

LimitRange: ✔ allowed (within min/max)
ResourceQuota: ❌ rejected (exceeds namespace totals)

---

# Best practices (production)

✅ Always use both
✅ Set `defaultRequest` smaller than `default`
✅ Set `max` conservatively
✅ Always define `requests` in production workloads
✅ Enforce quotas per team namespace

