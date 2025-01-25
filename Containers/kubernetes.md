# Kubernetes guide

Kubernetes (also called k8s) manages a highly available cluster of computers, working as a single unit. It allows you to deploy containerized applications across the cluster without binding them to specific machines. Applications must be containerized to leverage this model, offering greater flexibility and availability compared to traditional deployment methods where apps were tightly integrated into individual hosts. Kubernetes automates container distribution and scheduling efficiently. It is an open-source, production-ready platform.

A Kubernetes cluster has two main components:

- Control Plane: Manages and coordinates the cluster.

- Nodes: Worker machines that run applications.

## Start a cluster

To start a cluster there is several options based on the level of knowledge about kubernetes. For locally setup, you can use Docker Desktop, Rancher (alternative to Docker Desktop), minikube (for easy learning and dev with k8s) and kubeadm if you want a deeper control of the cluster configuration.

Here is the link to [installation minikube tutorial](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download) and the [official documentation of minikube](https://kubernetes.io/docs/tutorials/hello-minikube/).

with this you can manage you kubernetes cluster using this simple commands:

Pause Kubernetes without impacting deployed applications:

```bash
minikube pause
```

Unpause a paused instance:

```bash
minikube unpause
```

Halt the cluster:

```bash
minikube stop
```

Delete all of the minikube clusters:

```bash
minikube delete --all
```

## Kubernetes basics

to get the version of kubernetes run:

```bash
kubectl version
```

if you want to know how the cluster was created, run:

```bash
kubectl config get-contexts
```

to get the information about the cluster, run:

```bash
kubectl cluster-info
```

view cluster configuration:

```bash
kubectl config view
```

view cluster events:

```bash
kubectl get events
```

to get the list of nodes:

```bash
kubectl get nodes
```

to get the list of pods:

```bash
kubectl get pods
```

to delet all the pods in a specific namespace:

```bash
kubectl delete --all deployments --namespace=foo 
```

to get a list of namespaces (a namespace is a way to organize clusters into virtual sub-clusters):

```bash
kubectl get namespaces
```

## Running conteneraized applications

To create a new cluster connection run this command:

```bash
kubectl config set-cluster my-cluster --server=127.0.0.1:8087
```

To connect to the cluster, it is necessary to provide an authentication method. There are several options to authenticate with the cluster:

Using a token:

```bash
kubectl config set-credentials my-user --token=Py93bt12mT
```

Using basic authentication:

```bash
kubectl config set-credentials my-user --username=your-username --password=yout-password
```

Using a certificate:

```bash
kubectl config set-credentials my-user --client-certificate=my-certificate.crt --client-key=my-key.key
```

A context is a collection of access parameters that defines how to connect to a specific cluster.

To create a new context:

```bash
kubectl config set-context --cluster=my-cluster --user=my-user
```

In a kubectl context, it is possible to set a namespace. If provided, then any command would be executed in that namespace. The following command creates a context that points to the namespace.

```bash
kubectl config set-context my-context --cluster=my-cluster --user=my-user --namespace=redhat-dev
```

You can select a context by running:

```bash
kubectl config use-context my-context
```

## Creating a Deployment

A Kubernetes pod is a group of one or more Containers, sharing administration and networking. In this tutorial, the Pod contains a single Container. A Kubernetes Deployment monitors the Pod's health and restarts its Container if it fails. Deployments are the preferred method for managing Pod creation and scaling.

Use kubectl create deployment to deploy con

```bash
kubectl create deployment deployment-name --image image --replicas=3
```

To see the manifiest of a specific deployment, run:

```bash
kubectl get deployment deployment-name -o yaml
```

if you want to edit the manifiest, you can run this command:

```bash
kubectl edit deployment deployment-name
```

to scale a deployment (replace deployment-name and n):

```bash
kubectl scale deployment deployment-name --replicas=n
```

get the log of a specific deployment by his id:

```bash
kubectl logs node-id
```

## Kubernetes services: networking

## Docker-compose migration to Kubernetes

This guide is based on the [official documentation](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/). Komposer is a tool that allow you to convert a docker-compose file into a several kubernetes manifests. Maybe will not be a perfect conversion, but definitely will save you time.

You need to have a Kubernetes cluster, and the kubectl command-line tool must be configured to communicate with your cluster.

Then is need to install Kompose, a conversion tool for all things compose to container orchestrators.

for MacOS:

```bash
brew install kompose
```

To convert the docker-compose.yml file to files that you can use with kubectl, run kompose convert and then kubectl apply -f output file.

```bash
kompose convert
```

or to create a Chart to be used with Helm

```bash
kompose convert -c
```

and then run the manifiest that was created in previous step. Replace the current yamls with your owns manifiest files.

```bash
 kubectl apply -f web-tcp-service.yaml,redis-leader-service.yaml,redis-replica-service.yaml,web-deployment.yaml,redis-leader-deployment.yaml,redis-replica-deployment.yaml
```