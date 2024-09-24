# Docker & Docker Compose Cheat Sheet

## Docker

### 1. Gestión de Imágenes

- Ver imágenes descargadas:
  ```bash
  docker images
  ```

- Descargar una imagen:
  ```bash
  docker pull <image-name>

- Eliminar una imagen:
  ```bash
  docker rmi <image-id>

### 2. Gestión de Contenedores

- Correr un contenedor:
  ```bash
  docker run -d -p <host-port>:<container-port> <image-name>

- Correr un contenedor con nombre:
  ```bash
  docker run -d --name <container-name> -p <host-port>:<container-port> <image-name>

- Ver contenedores en ejecución:
  ```bash
  docker ps
  ```

- Ver todos los contenedores (incluso detenidos):
  ```bash
  docker ps -a
  ```

- Detener un contenedor:
  ```bash
  docker stop <container-id>
  ```

- Eliminar un contenedor:
  ```bash
  docker rm <container-id>
  ```

- Eliminar un contenedor en ejecución:
  ```bash
  docker rm -f <container-id>
  ```

### 3. Interacción con Contenedores

- Ejecutar un comando dentro de un contenedor en ejecución:
  ```bash
  docker exec -it <container-id> <command>
  ```
  
- Abrir una terminal dentro del contenedor:
  ```bash
  docker exec -it <container-id> /bin/bash
  ```
  
- Ver logs de un contenedor:
  ```bash
  docker logs <container-id>
  ```
  
- Copiar archivos del contenedor al host:
  ```bash
  docker cp <container-id>:/path/in/container /path/on/host
  ```
  
### 4. Limpieza y Mantenimiento

- Eliminar contenedores detenidos:
  ```bash
  docker container prune
  ```
  
- Eliminar todas las imágenes no usadas:
  ```bash
  docker image prune -a
  ```
  
- Eliminar todos los volúmenes no usados:
  ```bash
  docker volume prune
  ```
  
- Eliminar todo (contenedores, imágenes, volúmenes, redes):
  ```bash
  docker system prune -a
  ```
  
---

## Docker Compose

### 1. Comandos Básicos de Docker Compose

- Iniciar servicios definidos en docker-compose.yml:
  ```bash
  docker-compose up
  ```
  
- Iniciar servicios en modo "detached" (en segundo plano):
  ```bash
  docker-compose up -d
  ```
  
- Detener servicios:
  ```bash
  docker-compose down
  ```
  
### 2. Gestión de Servicios

- Ver el estado de los contenedores de Docker Compose:
  ```bash
  docker-compose ps
  ```
  
- Reiniciar un servicio específico:
  ```bash
  docker-compose restart <service-name>
  ```
  
- Escalar un servicio a múltiples réplicas:
  ```bash
  docker-compose up -d --scale <service-name>=<num-replicas>
  ```
  
### 3. Logs y Diagnóstico

- Ver los logs de los servicios:
  ```bash
  docker-compose logs

- Ver los logs de un servicio específico:
  ```bash
  docker-compose logs <service-name>
  ```
  
### 4. Construcción y Actualización

- Construir o reconstruir los servicios:
  ```bash
  docker-compose build
  ```
  
- Reconstruir un servicio específico:
  ```bash
  docker-compose build <service-name>
  ```
  
- Reconstruir y levantar servicios (forzando nueva construcción):
  ```bash
  docker-compose up --build
  ```
  
### 5. Volúmenes y Redes

- Ver los volúmenes usados por los servicios:
  ```bash
  docker-compose volume ls
  ```
  
- Eliminar volúmenes creados por docker-compose:
  ```bash
  docker-compose down --volumes
  ```
  
- Ver las redes creadas por Docker Compose:
  ```bash
  docker network ls
  ```
  
---

## Tips Adicionales

- Actualizar contenedores sin interrupción:
  ```bash
  docker-compose up -d --no-deps --build <service-name>
  ```
  
- Acceder a un contenedor de Docker Compose:
  ```bash
  docker-compose exec <service-name> /bin/bash
  ```

- Eliminar contenedores, redes y volúmenes con Docker Compose:
  ```bash
  docker-compose down --rmi all --volumes --remove-orphans
  ```
---

### Recursos Adicionales

- [Documentación Oficial de Docker](https://docs.docker.com/)
- [Documentación Oficial de Docker Compose](https://docs.docker.com/compose/)
