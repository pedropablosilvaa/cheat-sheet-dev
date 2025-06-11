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

### Automatic formating

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

### Update configuration

Let's say that we need to change the port of our docker container from ```8000``` to ```8080```

```git
resource "docker_container" "nginx" {
  image = docker_image.nginx.latest
  name  = "tutorial"
  hostname = "learn-terraform-docker"
  ports {
    internal = 80
-   external = 8000
+   external = 8080
  }
}
```

Run ```terraform apply``` agaom to refresh state and see how your updates affect existing resources.

Execution plan symbols

```~/+``` (destroy and then create): indicates the resource will be replaced.

```~``` (in-place update): shows attributes Terraform can modify without replacement.

Approval prompt
Terraform pauses for your confirmation—type ```yes``` to proceed.

Terraform destroys the old container and creates a new one with the updated port. Afterwards, use ```terraform show``` to inspect the new resource values.

### Destroy the infrastructure

```terraform destroy```

Answer ```yes``` to execute this plan and destroy the infrastructure.

### Use variables

Create a new file called ```variables.tf``` with a block defining new ```container_name``` variable.

```json
variable "container_name" {
  description = "Value of the name for the Docker container"
  type        = string
  default     = "ExampleNginxContainer"
}
```

Also in main.tf, update the ```docker_container``` resources block using the new variable. The ````container_name``` variable block will default to its default value ("ExampleNginxContainer") unless you declare a different value.

```git
resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
- name  = "tutorial"
+ name  = var.container_name
  ports {
    internal = 80
    external = 8080
  }
}
```

To apply the configuration, just run ```terraform apply``` and tip ```yes``` to confirm.

Now apply the configuration again, this time overriding the default container name by passing in a variable using the -var flag. Terraform will update the container's name attribute with the new name. Respond to the confirmation prompt with yes.

### Manage outputs

It is possible to show some outputs when a configuration is applied. Let's say that we have a outputs.tf with the following configuration:

```json
output "container_id" {
  description = "ID of the Docker container"
  value       = docker_container.nginx.id
}

output "image_id" {
  description = "ID of the Docker image"
  value       = docker_image.nginx.id
}
```

Using ```terraform apply``` you can see the output in the CLI.

To query outputs jus use ```terraform output``` and outputs will be displayed in the CLI.