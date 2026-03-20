## Correct way

1. k create role pod-reader --verb=get,list,watch --resource=pods
2. k create rolebinding pod-reader-binding --role=pod-reader --serviceaccount=default:pod-reader-sa
3. k create serviceaccount pod-reader-sa
4. `
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
`
5. k exec -it test-pod -- sh
6. kubectl auth can-i list pods --as=system:serviceaccount:default:pod-reader-sa
