## What Are Taints and Tolerations?

They work **together** to **control which pods can be scheduled on which nodes**.

* **Taint** → Applied **on a Node** to *repel* pods.
* **Toleration** → Applied **on a Pod** to *tolerate* that taint.

You can think of it as:

> “A tainted node says: *Only specific pods that can tolerate me are allowed here.*”


## Example

### Step 1: Add a Taint to a Node

```bash
kubectl taint nodes node1 key=value:NoSchedule
```

This means:

* The node `node1` **will not accept new pods**
* **Unless** those pods have a **matching toleration**.

---

### Step 2: Pod with Matching Toleration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: toleration-pod
spec:
  containers:
  - name: nginx
    image: nginx
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
```

✅ This pod **can** be scheduled on `node1`
❌ Any other pod **cannot** be scheduled there.


## Types of `effect`

| Effect             | Meaning                                                                          |
| ------------------ | -------------------------------------------------------------------------------- |
| `NoSchedule`       | Do **not** schedule pods here unless they tolerate the taint.                    |
| `PreferNoSchedule` | Try **to avoid** placing pods here (soft rule).                                  |
| `NoExecute`        | New pods are not scheduled **and** existing non-tolerating pods are **evicted**. |

---

## Removing a Taint

```bash
kubectl taint nodes node1 key=value:NoSchedule-
```

(Note the `-` at the end — that removes it.)


## Real-World Use Cases

| Scenario                        | Example                                                                |
| ------------------------------- | ---------------------------------------------------------------------- |
| Dedicated nodes for system pods | Taint worker nodes and allow only `kube-system` pods to tolerate them. |
| GPU nodes                       | Taint GPU nodes so only ML workloads with tolerations can run there.   |
| Isolating environments          | Taint nodes for “test”, “prod”, etc. environments.                     |


### Summary Table

| Concept        | Applied On                                | Purpose                                     |
| -------------- | ----------------------------------------- | ------------------------------------------- |
| **Taint**      | Node                                      | Restrict pods from running unless tolerated |
| **Toleration** | Pod                                       | Allow scheduling on tainted nodes           |
| **Effect**     | NoSchedule / PreferNoSchedule / NoExecute | Defines taint behavior                      |
