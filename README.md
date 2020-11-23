# RetinaX

RetinaX: A web platform for simulation and analysis of a network model of direction selectivity in the retina

## Technologies

- Java 11
- Vue 2
- Spring Boot 2
- Mongodb
- Python 2

## Enviroment and requirements

- **docker**. In order to build docker images. (https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 -> follow steps 1 and 2 of this tutorial)
- **docker-compose** In order to deploy a local enviroment (https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-es -> make sure of install docker first)

## Deployment

RetinaX has 3 main modules. Each of them has a single Dockerfile that can be built with any name and can be deployed "anywhere". It's highly recommended to name them with their root folder name when deploying in a production enviroment.

The easiest way to deploy the platform is just using the available docker-compose.yml file at root folder

In order to making the deployment process easier you can use the available "build-docker.sh" shell script at root folder

Just run:

```
./build-docker.sh
```

And the script will do the trick. 

Note: If you have problems or errors running the script, make sure of giving the proper permissions to it. (eg. running the command with "sudo" on linux)

After deploying the platform, you can access to the Client web application at:

```
http://{HOST}:80
```
