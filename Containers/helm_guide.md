# HELM guide

## Core concepts

Helm is a package manager for Kubernetes that simplifies the deployment and management of applications by packaging Kubernetes resources into charts, allowing for easy installation, upgrade, and management of applications  across different environments.

- **Charts:** Charts are collections of files that describe a related set of Kubernetes resources, allowing you to package and deploy applications with ease.

- **Repository:** A place where charts can be collected and shared. It's like DockerHub, but for kubernetes packages.

- **Release:** It's an instance of a chart that is running in a K8s cluster. One chart can be installed several times into the same cluster. And each time it is installes, a new release is created. So if you want to install two instance of an application, each one will have its own release.

- **Templates:** Helm charts use templates to generate Kubernetes manifests, allowing for dynamic configuration and customization.

## Installation

[Official documentation](https://helm.sh/docs/intro/install/)

You can install HELM using binary files, from a script or via package managers like homebrew:

```bash
brew install helm
```

## Add Helm chart repository

The chart repository is a site where the helm charts are listed and ready to use. In a similar way that DockerHub works.

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Once you have added the repository, you can list the availabe charts you can install:

```bash
helm search repo bitnami
```

To install a chart, run ```helm install```

```bash
helm repo update #update list of latest charts
helm install bitnami/mysql --generate-name
```

To get the list of helm charts running, use:

```bash
helm list
```

To uninstall a release use ```helm uninstall``` command:

```bash
helm uninstall mysql
```

