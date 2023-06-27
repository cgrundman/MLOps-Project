FROM python:3.9-slim-bookworm

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    pip install git+https://github.com/JustAnotherArchivist/snscrape.git && \
    pip install Flask==2.1.2 && \
    pip install requests==2.27.1

EXPOSE 5000

COPY ./server /

CMD ["python", "server.py"]