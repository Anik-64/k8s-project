# Understanding Kubernetes Requests & Limits

Let’s explore the essentials of Requests and Limits, why they matter, and how to use them effectively.

## What's the Deal with Requests & Limits?

Think of your Kubernetes cluster as a bustling city and pods as tenants in an apartment building. Each tenant (pod) requires specific resources like CPU and memory to function:

- **Requests**: This is the minimum amount of resources a pod needs to operate smoothly. Think of it as a guaranteed reservation for the pod.
- **Limits**: This is the maximum amount of resources a pod can use. It acts as a safety cap to prevent any pod from consuming more than its fair share and disrupting others.

## Why are Requests & Limits Important?

- **Resource Control**: By setting limits, you prevent a single pod from monopolizing resources, which can lead to issues like out-of-memory (OOM) kills or CPU starvation.  
> ☠️ Why OOM can be a good thing? Because it kills the pod;  
otherwise, the container would have consumed all the memory and could kill the node. Killing the pod is a better option than killing a node itself.
- **Predictability**: Requests help the scheduler allocate resources efficiently and ensure pods have the necessary resources to run effectively.