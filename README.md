# Cross-Namespace Pod Communication in Kubernetes

## Overview
This setup demonstrates how pods in **different namespaces** can communicate with each other using **Services (ClusterIP)**.

Kubernetes allows direct pod-to-pod communication using **pod IPs**, but when communication goes through **ClusterIP Services**, DNS resolution and proper service naming become important.

## Scenario
- **Namespaces:** `demo`, `test`
- Each namespace has:
  - A **Deployment** (3 replicas of `nginx`)
  - A **Service** of type `ClusterIP`

Example:
```bash
demo/
  ├─ demo-nginx (Deployment)
  └─ demo-service (ClusterIP)

test/
  ├─ test-nginx (Deployment)
  └─ test-service (ClusterIP)
```

## Problem

While pod-to-pod communication using **pod IPs** works fine,
trying to communicate via **service names** across namespaces fails, e.g.:

```bash
curl test-service
curl test-service.test.svc.cluster.local
```

results in:

```bash
curl: (6) Could not resolve host: test-service
```

## Reason

Each pod’s `/etc/resolv.conf` file defines the **DNS search domain** for that namespace:

```bash
cat /etc/resolv.conf
search demo.svc.cluster.local svc.cluster.local cluster.local
nameserver 10.96.0.10
options ndots:5
```

This means:

* Inside the `demo` namespace, DNS searches default to `demo.svc.cluster.local`.
* To reach a service in another namespace, you must specify the **full FQDN**:

  ```
  <service-name>.<namespace>.svc.cluster.local
  ```

## Solution

From a pod inside the `demo` namespace:

```bash
curl test-service.test.svc.cluster.local
```

From a pod inside the `test` namespace:

```bash
curl demo-service.demo.svc.cluster.local
```

This uses Kubernetes DNS resolution to correctly route the request to the target service.

## Notes

* ClusterIP services are **internal-only**, accessible only within the cluster.
* Pod IPs may change on restarts, but service names remain stable.
* You can verify DNS configuration with:

  ```bash
  kubectl exec -it <pod> -n <namespace> -- cat /etc/resolv.conf
  ```
* You can check if the service has endpoints:

  ```bash
  kubectl get endpoints -n <namespace>
  ```

## Summary

| Communication Type                                 | Works? | Notes                                   |
| -------------------------------------------------- | ------ | --------------------------------------- |
| Pod-to-pod via Pod IP                              | ✅      | Direct IP communication                 |
| Pod-to-pod via Service name (same namespace)       | ✅      | Works automatically                     |
| Pod-to-pod via Service name (different namespaces) | ⚠️     | Use FQDN `<svc>.<ns>.svc.cluster.local` |
| Pod-to-pod via ClusterIP                           | ❌      | Not recommended, use DNS names          |

---

**Author:** *Anik Majumder*  
**Purpose:** Demonstration of inter-namespace communication using ClusterIP services.

