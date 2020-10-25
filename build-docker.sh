#!/usr/bin/env bash
set -e

echo "Building services. Please wait..."

###Compile simulator middleware
echo "Building middleware service"

cd simulationMiddleware

docker run -v "$PWD":/usr/src/mymaven -v "$HOME/.m2":/var/maven/.m2 -w /usr/src/mymaven -ti --rm -u $UID \
  -e MAVEN_CONFIG=/var/maven/.m2 \
  maven:3.6.3-jdk-11-slim \
  mvn -Duser.home=/var/maven -DskipTests -V -U -e --batch-mode clean package

cd ..  

###Run docker enviroment
echo "Running docker enviroment"
docker-compose up -d