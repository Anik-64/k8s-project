## What is **Affinity** in Kubernetes?

**Affinity** = rules that tell the Kubernetes **scheduler** *where* a Pod **should or should not be placed**, based on labels of nodes or other pods.

It’s like saying:

> “I prefer or require my Pod to run on a node (or near another Pod) that matches certain conditions.”

## There are **two main types of Affinity**:

### 1️⃣ **Node Affinity**

→ Controls **which nodes** a pod can or should run on.

Works similar to `nodeSelector`, but **more flexible** — supports both **hard (required)** and **soft (preferred)** rules.

#### Example:

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: disktype
          operator: In
          values:
          - ssd
```

**Meaning:**

> Only schedule this pod on nodes where `disktype=ssd`.

You can also use:

```yaml
preferredDuringSchedulingIgnoredDuringExecution:
```

to express **preference** instead of a hard requirement.

### 2️⃣ **Pod Affinity & Pod Anti-Affinity**

→ Controls **which pods** your pod prefers (or avoids) to be scheduled **with or away from**.

#### **Pod Affinity (together)**

> “Place me near pods with these labels.”

Example:

```yaml
affinity:
  podAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - frontend
      topologyKey: "kubernetes.io/hostname"
```

**Meaning:**

> Schedule this pod on the same node as another pod with label `app=frontend`.

#### **Pod Anti-Affinity (separate)**

> “Do NOT place me near pods with these labels.”

Example:

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - backend
        topologyKey: "kubernetes.io/hostname"
```

**Meaning:**

> Prefer not to schedule this pod on the same node as a pod labeled `app=backend`.

## Summary Table

| Type                  | Applies To | Purpose                     | Example Use Case                 |
| --------------------- | ---------- | --------------------------- | -------------------------------- |
| **Node Affinity**     | Node       | Place pod on specific nodes | Run only on `ssd` or `gpu` nodes |
| **Pod Affinity**      | Other Pods | Group pods together         | Frontend near backend            |
| **Pod Anti-Affinity** | Other Pods | Spread pods apart           | One replica per node for HA      |

All affinities can use these rule types:

* `requiredDuringSchedulingIgnoredDuringExecution` → **hard rule**
* `preferredDuringSchedulingIgnoredDuringExecution` → **soft preference**
