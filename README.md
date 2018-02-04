# masterbuttons

## Requirements
To run the server you need [Docker](https://www.docker.com/community-edition#/download) and [Docker compose](https://docs.docker.com/compose/install/) (already installed with docker for windows and mac)

## Execute
Download the repository and execute run.sh, this will build the project, execute unit tests, create the docker image and execute the project inside a container. You should be able to see the swagger interface for the api in [localhost at port 80](http://localhost)

You can change the port mapping at docker-compose.yml

The entry point of the application is src/mastermind/api.py
