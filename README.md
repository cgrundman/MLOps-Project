# MLOps-Project

Introductory Project to introduce MLOps material

## Dockerize the Server

Switch to the project-directory and run the following command to build the docker image:

```bash
docker build twitter_sentiments_server .
```

## Run the container

Now that the image has been successfully built you can run a container out of it. You can do so by using the following command:

```bash
docker run --rm \
-p 5000:5000 \
--mount src="$(pwd)"/model,target=/model,type=bind \
twitter_sentiments_server
```
