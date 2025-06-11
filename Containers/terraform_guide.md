# terraform

Create a directry named learn-terraform-docker-container

```bash
mkdir learn-terraform-docker-container
```

go to that directory

```bash
cd learn-terraform-docker-container
```

Create a file to define the infrastructure

```bash
touch main.tf
```

copy the following text into file:

```json
terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "tutorial"
  ports {
    internal = 80
    external = 8000
  }
}
```

## Principal parts of the configuration file

- terraform {} block: Specifies Terraform settings and required providers. Each provider entry includes a source (e.g., kreuzwerker/docker → registry.terraform.io/kreuzwerker/docker) and an optional version constraint to lock provider versions and ensure compatibility.

- provider block: Configures a specific provider plugin (here, Docker). You can define multiple provider blocks to manage resources across different platforms and even chain outputs between them (e.g., pass a Docker image ID into Kubernetes).

- resource blocks: Declare the actual infrastructure components. Each block is identified by ```<type>.<name>``` (e.g., docker_image.nginx), where the type’s prefix matches the provider. Inside, you set arguments (like image names, ports, instance sizes) that control how Terraform creates or manages the resource.

## Cheat sheet

### Initialize the repository

Initialize the reposiutory using ```terraform init```. Initializing a configuration directory downloads and installs the providers defined in the configuration, which in this case is the docker provider.

### automatic formating

Automatic formatting: Use ```terraform fmt``` to apply a consistent style to your ```.tf``` files; it adjusts indentation and alignment according to Terraform conventions.

Validation: Run ```terraform validate``` to check that your configuration is syntactically correct and internally consistent. A “Success!” message indicates there are no errors.

### Create the infrastructure

Run ```terraform apply``` to generate and display the execution plan (which resources will be added, changed, or destroyed). Resources marked with a ```+ create``` (e.g., ```docker_image.nginx``` and ```docker_container.nginx```) will be created. Terraform pauses for confirmation—type ```yes```to proceed and provision the image and container.

### Verify

After apply completes, visit ```http://localhost:8000``` to confirm the Nginx container is running.

### State management

Terraform records resource IDs and metadata in ```terraform.tfstate``` to track managed infrastructure. As this file can contain sensitive data, secure it appropriately or use a remote backend in production.

### Inspecting state

```terraform show```: Displays detailed information about all managed resources.

```terraform state list```: Lists the resource addresses currently tracked in the state (e.g., ```docker_image.nginx```, ```docker_container.nginx```).

### Destroy the infrastructure

```terraform destroy```
