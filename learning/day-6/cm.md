## What is a ConfigMap?

A **ConfigMap** is a Kubernetes object used to **store configuration data** in **key-value** pairs.
It allows you to **separate configuration** from application code — so you don’t have to rebuild or redeploy your image when configuration changes.

## Advantages

1. **Separation of concerns**

   * Keeps config out of the container image — no need to rebuild the image for simple config changes.

2. **Dynamic configuration**

   * You can update configuration (ConfigMap) without changing app code.

3. **Centralized management**

   * One ConfigMap can be used by multiple pods, ensuring consistent configuration.

4. **Multiple ways to use**

   * As environment variables, command-line arguments, or mounted as files inside the container.

5. **Integration with CI/CD tools**

   * Works well with tools like ArgoCD or Jenkins for managing environment-specific settings.

## Disadvantages

1. **No automatic pod reload**

   * If you update a ConfigMap, the running pods **won’t automatically reload** — you need to restart the pods or trigger a rollout.

2. **Not suitable for sensitive data**

   * Data in ConfigMaps is **not encrypted**, only base64-encoded.
     Use **Secrets** for passwords or tokens instead.

3. **Limited size**

   * Maximum size per ConfigMap is about **1MB**.

4. **Version control complexity**

   * Frequent config updates can clutter YAML management if not handled carefully.

## In short:

| Feature         | Description                                          |
| --------------- | ---------------------------------------------------- |
| Purpose         | Store non-confidential config data in key-value form |
| Used By         | Pods and Deployments                                 |
| Access Methods  | Environment variables, files, or command args        |
| Sensitive Data? | ❌ No (use Secret)                                    |
| Auto Reload?    | ❌ No (manual restart needed)                         |
