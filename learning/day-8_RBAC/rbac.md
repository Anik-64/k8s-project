# **RBAC in Kubernetes**

RBAC = **Role-Based Access Control**
It controls:

### ✔ Who can access the cluster

### ✔ What they can do

### ✔ Where they can do it (namespace or cluster-wide)

Kubernetes uses RBAC (Roles, RoleBinding, ClusterRoles, ClusterRoleBindings) to enforce permissions.

---

# **1. Role**

A **Role** gives **permissions for a specific namespace**.

### Meaning:

A **Role works only inside a single namespace**.

### Example permissions inside namespace `default`:

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

* read-only access to pods
* **only in the default namespace**

A Role **cannot** give access outside its namespace.

---

# **2. RoleBinding**

RoleBinding = **Attaches a Role to a user or group**.

It tells Kubernetes:

> “This user is allowed to use this role’s permissions.”

### Example:

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: anik
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### What this means:

User **anik** can read pods **only in the default namespace**.

---

# **3. ClusterRole**

A **ClusterRole** gives permissions **across the entire cluster**.

### Meaning:

A ClusterRole:  

✔ Works in *all namespaces*  
✔ Can include non-namespaced resources (nodes, PVs etc.)  

Example:

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: view-nodes
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", list]
```

This allows reading **nodes**, which is a cluster-wide resource.

ClusterRoles can also define namespace permissions but are available across the cluster.

---

# **4. ClusterRoleBinding**

ClusterRoleBinding = attach ClusterRole to a user or group — **cluster-wide**.

Example:

```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: all-nodes-reader
subjects:
- kind: User
  name: anik
roleRef:
  kind: ClusterRole
  name: view-nodes
```

This gives user **anik** access to read **nodes across the entire cluster**.

---

# **Big Differences**

| RBAC Component         | Scope        | Purpose                                                |
| ---------------------- | ------------ | ------------------------------------------------------ |
| **Role**               | Namespace    | Permissions in one namespace                           |
| **RoleBinding**        | Namespace    | Binds Role → user in that namespace                    |
| **ClusterRole**        | Cluster-wide | Permissions across all namespaces or cluster resources |
| **ClusterRoleBinding** | Cluster-wide | Binds ClusterRole → user for entire cluster            |

---

#  How They Work Together 

1. **User logs in** using certificate/token
2. Kubernetes reads the user identity
3. RBAC checks the user’s *bindings*
4. From bindings, it finds the *role or clusterrole*
5. Role/ClusterRole contains the allowed verbs (“get”, “list”, “create”)
6. The API server says **allowed** or **forbidden**

---

# Summary 

> **Role & RoleBinding = namespace-level access**  
> **ClusterRole & ClusterRoleBinding = cluster-wide access**  

# Diagram

https://app.eraser.io/workspace/0HjEEBtv3M5GJKz078mi?origin=share