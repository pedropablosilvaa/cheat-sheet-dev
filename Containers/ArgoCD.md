# Argo CD guide

ArgoCD Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes (k8s).

This is a guide to install and use ArgoCD. This guide is based in the folowing [official documentation.](https://argo-cd.readthedocs.io/)

## Getting started

### Install ArgoCD

First, create a namespace called argocd and deploy ArgoCD service and application using a manifest file:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

This installation will have a self-signed certificate and cannot be accessed witout a bit of extra work ([see the documentation](https://argo-cd.readthedocs.io/en/stable/getting_started/))

### Install ArgoCD CLI

```bash
brew install argocd
```

### Access the argo CD API Server

By default, the Argo CD API server is not exposed with an external IP. To access the API server, choose one of the following techniques to expose the Argo CD API server:

#### Service Type Load Balancer

Change the argocd-server service type to LoadBalancer:

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

#### Ingress

[ingress documentation](https://argo-cd.readthedocs.io/en/stable/getting_started/#:~:text=ingress%20documentation)

#### Port Forwarding

To access API server from https://localhost:8080

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

