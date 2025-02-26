# Argo CD guide

ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes (k8s).

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

### Login Using The CLI

When ArgoCD is initialized a auto-generated passowrd is set by default. This password is stored in a secret named ```argocd-initial-admin-secret``` in the argocd installation namespace. To get this password use argocd CLI:

```bash
argocd admin initial-password -n argocd
```

with the output of the above cli command, login into ArgoCD IP or hostname:

```bash
argocd login <ARGOCD_SERVER>
```

if your are running this in a localhost:

```bash
argocd login localhost:8080
```

then, update your password:

```bash
argocd account update-password
```

### Create an app from a git repository

#### Create app via CLI

Set the current namespace to argocd running:

```bash
kubectl config set-context --current --namespace=argocd
```

Create the example guestbook app (change the repo by that one you want to manage):

```bash
argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default
```

### Sync (Deploy) the app

#### Syncing via CLI

get the current sync status

```bash
argocd app get guestbook
```

sync the app:

```bash
argocd app sync guestbook
```