#!/bin/bash

IMAGE="ghcr.io/charl56/jukebox-public:latest"
CONTAINER="jukebox"
PORT="5025:5025"
VOLUME_PATH="/home/user/jukebox/data"
CONTAINER_PATH="/app/static"

echo "Starting Jukebox"

# Create folder, if not exist
mkdir -p $VOLUME_PATH

# Stop and remove old container
docker stop $CONTAINER 2>/dev/null
docker rm $CONTAINER 2>/dev/null

# Check if volume is empty
if [ -z "$(ls -A $VOLUME_PATH 2>/dev/null)" ]; then
    echo "Volume is empty, initialing data..."
    
    # Lancer temporairement le conteneur sans volume pour extraire les fichiers
    docker run --name temp_container -d ghcr.io/charl56/jukebox-public:latest
    docker cp temp_container:/app/static/. $VOLUME_PATH

    docker stop temp_container
    docker rm temp_container
    
    echo "Init ready"
fi

# Lancer le conteneur final avec le volume
docker run -d --name $CONTAINER --privileged -p $PORT -v $VOLUME_PATH:$CONTAINER_PATH -v /dev/gpiomem:/dev/gpiomem -d $IMAGE --restart=always 