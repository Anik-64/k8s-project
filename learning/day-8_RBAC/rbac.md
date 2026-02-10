# **RBAC in Kubernetes**

RBAC = **Role-Based Access Control**

It controls:

### ✔ Who can access the cluster

### ✔ What they can do

### ✔ Where they can do it (namespace or cluster-wide)

Kubernetes enforces RBAC using:

* **Role**
* **RoleBinding**
* **ClusterRole**
* **ClusterRoleBinding**
* **ServiceAccount** (identity for applications)

# **Who Can Be Granted Access? (Very Important)**

RBAC permissions are granted to **subjects**:

| Subject Type       | Used For                    |
| ------------------ | --------------------------- |
| **User**           | Humans (admins, developers) |
| **Group**          | Collection of users         |
| **ServiceAccount** | Applications / Pods         |

**RBAC does NOT create users**  
It only **authorizes identities**

# **1. ServiceAccount**

A **ServiceAccount (SA)** is an **identity for Pods**, not humans.

### Why ServiceAccount exists?

Pods need to:

* Talk to Kubernetes API
* Read ConfigMaps
* Watch Pods
* Create Jobs, etc.

They **should not use admin credentials**.

## Default behavior

If you don’t specify a ServiceAccount:

```text
Pod uses: default ServiceAccount
```

This is **bad practice** for production.

## Create a ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-reader-sa
  namespace: default
```

✔ Creates an identity
✔ No permissions yet

# **2. Role**

A **Role** defines **what actions are allowed** **Only inside one namespace**

### Example: Read Pods in `default`

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pod-reader
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

### This role allows:

✔ Read-only access to Pods  
✔ Only in `default` namespace  

Cannot access other namespaces

# **3. RoleBinding**

RoleBinding = **Connects a Role to a subject**

> “This identity can use this role”

## 🔹 RoleBinding for a USER

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods-user
  namespace: default
subjects:
- kind: User
  name: anik
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

✔ User `anik` can read pods in `default`

## 🔹 RoleBinding for a SERVICEACCOUNT (Most Common)

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods-sa
  namespace: default
subjects:
- kind: ServiceAccount
  name: pod-reader-sa
  namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

✔ Pods using `pod-reader-sa` can read pods
✔ Only in `default` namespace

# **4. Using ServiceAccount in a Pod**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  serviceAccountName: pod-reader-sa
  containers:
  - name: busybox
    image: busybox
    command: ["sh", "-c", "sleep 3600"]
```

### What happens automatically?

✔ Kubernetes mounts a token
✔ Pod authenticates as:

```
system:serviceaccount:default:pod-reader-sa
```

✔ RBAC is applied using that identity

# **5. ClusterRole**

A **ClusterRole** defines permissions **cluster-wide**

✔ All namespaces
✔ Cluster-scoped resources (nodes, PVs)

### Example: Read Nodes

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: view-nodes
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list"]
```

# **6. ClusterRoleBinding**

ClusterRoleBinding = attach ClusterRole to a subject **for the whole cluster**

## Example: User access

```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nodes-reader
subjects:
- kind: User
  name: anik
roleRef:
  kind: ClusterRole
  name: view-nodes
  apiGroup: rbac.authorization.k8s.io
```

## Example: ServiceAccount cluster access

```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: sa-nodes-reader
subjects:
- kind: ServiceAccount
  name: pod-reader-sa
  namespace: default
roleRef:
  kind: ClusterRole
  name: view-nodes
  apiGroup: rbac.authorization.k8s.io
```

✔ Any pod using this SA can read nodes

# **Big Differences (Updated)**

| Component          | Scope     | Used By   | Purpose                   |
| ------------------ | --------- | --------- | ------------------------- |
| Role               | Namespace | User / SA | Namespace permissions     |
| RoleBinding        | Namespace | User / SA | Attach Role               |
| ClusterRole        | Cluster   | User / SA | Cluster permissions       |
| ClusterRoleBinding | Cluster   | User / SA | Attach ClusterRole        |
| ServiceAccount     | Namespace | Pods      | Identity for applications |

# **How Everything Works Together (FLOW)**

1. Pod starts
2. Pod uses **ServiceAccount**
3. Kubernetes mounts SA token
4. Pod calls Kubernetes API
5. API Server identifies the subject
6. RBAC checks:

   * RoleBinding / ClusterRoleBinding
7. Role / ClusterRole defines allowed actions
8. Request is **Allowed or Forbidden**

# **Real-World Scenarios**

### ✅ App needs to read ConfigMaps

→ ServiceAccount + Role + RoleBinding

### ✅ Controller needs cluster-wide access

→ ServiceAccount + ClusterRole + ClusterRoleBinding

### ❌ Never use admin credentials inside Pods

# **Best Practices**

✔ One ServiceAccount per application  
✔ Least privilege (smallest verbs & resources)  
✔ Prefer Role over ClusterRole  
✔ Never bind `cluster-admin` casually  
✔ Use `kubectl auth can-i` to verify access  

# **Summary (Very Important)**

> **Users = humans**
> **ServiceAccounts = applications**
> **RBAC only authorizes, never creates identities**

# **Diagram (Identity → RBAC → Permission)**

[https://app.eraser.io/workspace/0HjEEBtv3M5GJKz078mi?origin=share](https://app.eraser.io/workspace/0HjEEBtv3M5GJKz078mi?origin=share)
