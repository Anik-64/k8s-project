# Kubernetes Project Repository

Welcome to my Kubernetes learning and practice repository! This repository contains various Kubernetes YAML configuration files and hands-on learning materials that demonstrate different K8s concepts and components.

## Overview

This repository serves as a comprehensive collection of Kubernetes configurations and learning resources. Whether you're new to Kubernetes or looking to deepen your understanding, you'll find practical examples and organized learning materials here.

## Repository Structure

### Kubernetes Configuration Files

The root directory contains YAML configuration files for various Kubernetes objects:

- **Pods** - Basic pod configurations and multi-container pod examples
- **Deployments** - Deployment manifests for application management
- **Services** - Service configurations (ClusterIP, NodePort, LoadBalancer)
- **Volumes** - Persistent Volume (PV) and Persistent Volume Claim (PVC) configurations
- **ConfigMaps** - Configuration data management
- **Secrets** - Sensitive data management
- **RBAC** - Role-Based Access Control configurations (Roles, RoleBindings, ClusterRoles, ClusterRoleBindings)
- **CSR** - Certificate Signing Request examples

### Learning Folder

The `learning/` directory contains day-by-day learning materials organized into separate folders:

```
learning/
├── day-01/
│   └── topic.md
├── day-02/
│   └── topic.md
├── day-03/
│   └── topic.md
└── ...
```

Each day folder includes:
- Hands-on exercises and examples
- A `topic.md` file explaining the concepts covered that day
- Relevant YAML configurations specific to that day's learning

This structured approach makes it easy to follow along with my Kubernetes learning journey and understand the progression of concepts.

## 🚀 Getting Started

### Prerequisites

- Kubernetes cluster (minikube, kind, or cloud-based cluster)
- kubectl CLI tool installed and configured
- Basic understanding of containerization and Docker  

If you do not have any local cluster installed then do not worry abou this. There are multiple free labs are available online where you can practice the configuration files easily. They are providing the cluster setup.
Like as:  
- [KodeKloud Kubernetes Playgrounds](https://kodekloud.com/public-playgrounds)  
- [Killercoda Playgrounds](https://killercoda.com/)  
- For CKS, CKA, CKAD, LFCS Simulators [Killershell](https://killer.sh/)  

### Using These Configurations

1. Clone this repository:
   ```bash
   git clone https://github.com/Anik-64/k8s-project.git
   cd k8s-project
   ```

2. Apply any configuration file:
   ```bash
   kubectl apply -f <filename>.yaml
   ```

3. Verify the resource creation:
   ```bash
   kubectl get <resource-type>
   ```

## 📖 Learning Path

If you're using this repository to learn Kubernetes, I recommend:

1. Start with the `learning/` folder and go through each day sequentially
2. Read the `topic.md` file in each day's folder to understand the concepts
3. Try out the YAML configurations provided
4. Experiment by modifying the configurations to deepen your understanding

