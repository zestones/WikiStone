#!/bin/bash

# Set colors for warning and user prompt messages
WARNING='\033[1;31m'
PROMPT='\033[1;33m'
NC='\e[0m' # No Color

# Print warning message in yellow
echo -e "${WARNING}WARNING: THIS WILL REMOVE EVERYTHING IN YOUR DOCKER"
echo -e "---------------------------------------------------${NC}\n"
# Ask user if they want to stop all running containers
echo -e "${PROMPT}Do you want to stop all running containers (y/n)?${NC} \c"
read answer

if [[ $answer =~ [Yy] ]]; then
  if [ "$(docker container ls -q)" ]; then
    docker container stop $(docker container ls -aq)
  else
    echo -e "No containers to stop.\n"
  fi
fi

# Ask user if they want to remove all containers
echo -e "${PROMPT}Do you want to remove all containers (y/n)?${NC} \c"
read answer

if [[ $answer =~ [Yy] ]]; then
  if [ "$(docker container ls -aq)" ]; then
    docker container rm $(docker container ls -aq)
  else
    echo -e "No containers to remove.\n"
  fi
fi

# Ask user if they want to remove all images
echo -e "${PROMPT}Do you want to remove all images (y/n)?${NC} \c"
read answer

if [[ $answer =~ [Yy] ]]; then
  if [ "$(docker image ls -q)" ]; then
    docker image rm $(docker image ls -aq)
  else
    echo -e "No images to remove.\n"
  fi
fi

# Ask user if they want to remove all volumes
echo -e "${PROMPT}Do you want to remove all volumes (y/n)?${NC} \c"
read answer

if [[ $answer =~ [Yy] ]]; then
  if [ "$(docker volume ls -q)" ]; then
    docker volume rm $(docker volume ls -q)
  else
    echo -e "No volumes to remove.\n"
  fi
fi