# MLOps-Project

This repository contains the project code for the MLOps course at opencampus.sh 2023. The objective of our project is to set up a containerized application on a raspberry pi to serve a trained language model.

For this project, we aim to train a suitable sentiment analysis model to analyse twitter posts.

## Components

Each participant worked on a different part of the project. We settled on the following main components to distribute the responsibilities:

1. Model Selection & Training: **Work in Progress** A language model of suitable size for a raspberry pi 4 shall be selected (e.g. from the Huggingface-Hub) and fine-tuned to conduct sentiment analysis.

2. Twitter Scraper: Building a TwitterScraper module that collects tweets from twitter based on a query and associated parameters. It returns the collected tweets along with some metadata (i.e. username, date likeCount etc...).

3. Server Application & Containerization: The Server Application is responsible for handling incoming requests, performing sentiment analysis using the trained model, and returning the results to the client. For easy deployment on a raspberry pi, the application will be put into a docker container.

4. GUI: A user interface has been implemented to make requests against the server. The python package tkinter was used to build a convenient GUI to enable the client side to send customized queries to the dockerized model.

## Testing the Application (for Development)

To run the server application and its associated container, follow these steps:

### Dockerize the Server (Build the Container)

Switch to the project-directory and run the following command to build the docker image:

```bash
docker build twitter_sentiments_server .
```

### Run the container

If the image has been successfully built you can run a container out of it. You can do so by using the following command:

```bash
docker run --rm \
-p 5000:5000 \
--mount src="$(pwd)"/model,target=/model,type=bind \
twitter_sentiments_server
```

### Access the API

Once the container is up and running, you can access the API by making HTTP requests to the `/predict`-endpoint under port 5000. You may use http://localhost:5000/predict if you run the container on your local computer or http://raspberrypi:5000/predict if you run it on a pi in your local network.

You can use **demo.ipynb** for a quick demonstration or you can run **user_interface.py** for accessing the API with the implemented GUI.

## Notes

Until now, model selection and training are still to be done. For demonstration purposes and for testing the application, a "naive" model is used, which outputs a random sentiment score between 0 and 1.

## Issues

There were a lot of changes and restrictions in Twitter and its API in the past months. Until now, we were using the `snscrape` module for collecting posts from Twitter. However, due to the instability of the platform and possibly unpredictable modifications that might come in the near future, the code in this project is prone to errors.
