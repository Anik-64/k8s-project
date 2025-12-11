# **Understanding the Basics First**

Kubernetes users **do not “exist” inside Kubernetes**.
They are **clients** who access the cluster (kubectl users).

To authenticate a real user, Kubernetes accepts:

### ✔ Client Certificates (MOST COMMON)

### ✔ Bearer Tokens

### ✔ ServiceAccounts (for pods)

For humans → we use **client certificates**.

# **Goal**

Create a new user **anik** who can authenticate to the cluster using a client certificate.


# **How Kubernetes Uses Certificates**

When you run:

```sh
kubectl get pods
```

Your kubectl sends a request to the API server with:

* Your **client certificate**
* Your **private key**

The API server checks:

1. Is this certificate signed by the cluster's **CA (Certificate Authority)**?
2. If yes → user is authenticated.
3. Then RBAC decides what the user can do (we ignore this for now).

# **What We Will Create**

For user **anik**, we will generate:

```
anik.key      → private key
anik.csr      → certificate signing request
anik.crt      → signed user certificate
```

Then we will add it to **kubeconfig** so kubectl can use it.

# **Step-by-Step Process**

## **STEP 1 — Create a Private Key for the User**

```sh
openssl genrsa -out anik.key 2048
```

This creates:

* A secret private key (never share)
* Used to sign the CSR

## **STEP 2 — Create CSR (Certificate Signing Request)**

```sh
openssl req -new -key anik.key -out anik.csr -subj "/CN=anik/O=dev-team"
```

Breakdown:

* **CN=anik** → username (**CN** means **Common Name**)
* **O=dev-team** → group (important later for RBAC) (**O** means **Organization**)

## **STEP 3 — Sign the CSR Using Kubernetes CA**

Where is Kubernetes CA?

On the control-plane node:

```
/etc/kubernetes/pki/ca.crt
/etc/kubernetes/pki/ca.key
```

Now sign:

```sh
openssl x509 -req -in anik.csr \
  -CA /etc/kubernetes/pki/ca.crt \
  -CAkey /etc/kubernetes/pki/ca.key \
  -CAcreateserial \
  -out anik.crt -days 365
```

🎉 This creates the **final certificate** → `anik.crt`.  
This **sign** code will create the anik.crt automatically but if you apply the **csr.yaml** file this will do the same thing

## **STEP 4 — Create a New User in Kubeconfig**

You tell kubectl to use the certificate:

```sh
kubectl config set-credentials anik \
  --client-certificate=anik.crt \
  --client-key=anik.key \
  --embed-certs=true
```

## **STEP 5 — Create a Context for User**

A context = cluster + user + namespace

```sh
kubectl config set-context anik \
  --cluster=kubernetes \
  --user=anik
```

Switch to the user:

```sh
kubectl config use-context anik
```

Now test:

```sh
kubectl get pods
```

You will probably get:

```
Error: forbidden
```

Why?
Because the user is authenticated but **does not have permissions**.

(This is where RBAC like RoleBinding comes in — we’re skipping that now.)

---

# **Flow Summary (Very Easy)**

### 1️⃣ Generate key

→ user’s personal private key

### 2️⃣ Generate CSR

→ a request to sign the certificate

### 3️⃣ Sign CSR with Kubernetes CA

→ creates the valid Kubernetes user certificate

### 4️⃣ Add user to kubeconfig

→ kubectl can now authenticate as that user

### 5️⃣ (Optional) Add permissions using RBAC

→ not covered yet

# **How to Verify the User Certificate**

```sh
openssl x509 -in anik.crt -text -noout
```

You will see:

* CN = anik
* O = dev-team
* Issuer = Kubernetes CA

