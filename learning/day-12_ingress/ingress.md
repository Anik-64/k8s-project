# Bare Metal NGINX Ingress Controller

Deploy the NGINX Ingress Controller on a bare-metal Kubernetes cluster:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.15.1/deploy/static/provider/baremetal/deploy.yaml
```
On bare metal, this creates a `NodePort` service for external access.
In cloud environments, the same deployment would typically create a `LoadBalancer` service.

Verify Service:
```yaml
root@controlplane:~$ k get svc/ingress-nginx-controller -n ingress-nginx 
NAME                       TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller   NodePort   10.102.121.151   <none>        80:31466/TCP,443:31743/TCP   25m
```

# Create Pods and Services

Create two sample applications (nginx and httpd) and expose them:
```bash
k run nginx --image=nginx --labels=app=nginx --port=80
k expose pod nginx --port=80 --name=nginx-service
k run httpd --image=httpd --labels=app=httpd --port=80
k expose pod httpd --port=80 --name=httpd-service
```

# Create Ingress Resource

Apply the ingress.yaml file.

>⚠️ Note: Initially, the annotations section was commented out. Without annotations, routing may not work correctly for custom paths.

Verify ingress and controller:
```yaml
root@controlplane:~$ k get svc/ingress-nginx-controller -n ingress-nginx 
NAME                       TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller   NodePort   10.110.48.71   <none>        80:31466/TCP,443:32626/TCP   6m12s
```

```yaml
root@controlplane:~$ k get ing
NAME         CLASS   HOSTS      ADDRESS      PORTS   AGE
my-ingress   nginx   anik.com   172.30.2.2   80      30m
```

# Host Resolution Issue

Trying to access the ingress:
```yaml
root@controlplane:~$ curl http://anik.com:31466/ngi
curl: (6) Could not resolve host: anik.com
```
Check `/etc/hosts`:
```yaml
root@controlplane:~$ cat /etc/hosts
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
127.0.0.1 ubuntu
127.0.0.1 host01
127.0.0.1 controlplane
172.30.2.2 node01
```
### Fix
Add a mapping for the ingress host:  
`172.30.2.2 anik.com`

# Issue: 404 Not Found

After fixing host resolution:  
```yaml
root@controlplane:~$ curl http://anik.com:31466/ing
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
```
```yaml
root@controlplane:~$ curl http://anik.com:31466/htpd
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body></html>
```
>At first glance, this may seem like an ingress issue - but it is not.

### Root Cause
- The ingress is working correctly.  
- The problem lies in path handling.  

By default:
- nginx serves content at /
- httpd serves content at /

However, ingress routes are defined as:

- /ngi
- /htpd

Since these paths don’t exist in the backend containers, they return *404 Not Found*.

# Solution: Use Rewrite Annotations
Uncomment and configure the annotations in ingress.yaml:
```yaml
annotations:
  nginx.ingress.kubernetes.io/rewrite-target: /
```
### What This Does

When a request comes in:

- /ngi -> rewritten to /
- /htpd -> rewritten to /

This allows the backend services to respond correctly.

# Final Result

Now the applications are accessible via ingress:

```yaml
root@controlplane:~$ curl http://anik.com:31466/htpd
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>It works! Apache httpd</title>
</head>
<body>
<p>It works!</p>
</body>
</html>
```
```yaml
root@controlplane:~$ curl http://anik.com:31466/ngi
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, nginx is successfully installed and working.
Further configuration is required for the web server, reverse proxy, 
API gateway, load balancer, content cache, or other features.</p>

<p>For online documentation and support please refer to
<a href="https://nginx.org/">nginx.org</a>.<br/>
To engage with the community please visit
<a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
For enterprise grade support, professional services, additional 
security features and capabilities please refer to
<a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

# Summary
- Bare metal ingress uses NodePort
- Hostname must be mapped in /etc/hosts
- 404 errors were caused by path mismatch, not ingress failure
- Fix achieved using rewrite annotations
