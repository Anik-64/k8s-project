## Correct way

1. k create role pod-reader --verb=get,list,watch --resource=pods
2. k create rolebinding pod-reader-binding --role=pod-reader --serviceaccount=default:pod-reader-sa
3. k create serviceaccount pod-reader-sa
4. 
```yaml
  apiVersion: v1  
kind: Pod  
metadata:  
  name: test-pod  
spec:  
  serviceAccountName: pod-reader-sa  
  containers:  
  - name: test  
    image: busybox  
    command: ["sleep", "3600"]  
```
5. k exec -it test-pod -- sh
6. kubectl auth can-i list pods --as=system:serviceaccount:default:pod-reader-sa

## ImagePullSecret with ServiceAccount

If you want to pull images from a private registry, you can create a secret and assign it to a service account.

1. **Create the Secret:**
   ```bash
   kubectl create secret docker-registry <secret-name> --docker-server=<server> --docker-username=<user> --docker-password=<pass> --docker-email=<email>
   ```

2. **Assign the Secret to the ServiceAccount:**
   ```yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: my-sa
   imagePullSecrets:
   - name: my-registry-key
   ```

3. **Use the ServiceAccount in a Pod:**
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-pod
   spec:
     serviceAccountName: my-sa
     containers:
     - name: my-container
       image: <private-image>
   ```
