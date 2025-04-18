# mini-RAG-App

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.8 or later

### Install Dependencies
```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```
### Install Python using MiniConda

1. Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2. Create a new environment using the following command:

```bash
$ conda create -n mini-rag-app python=3.8
```

3. Activate the environment:

```bash
$ conda activate mini-rag-app
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Run Docker Compose Services

```bash
$ `cd docker`
$ `cp .env.example .env`
```

- update `.env` with your credentails

```bash
$ cd docker
$ sudo docker compose up -d
```

### When is needed for clashes, use the following commands:

#### stop container

`sudo docker stop $(sudo docker ps -aq)`

#### remove stoped container

`sudo docker rm $(sudo docker ps -aq)`

#### remove images

`sudo docker rmi $(sudo docker images -q)`

#### clean the environment

`sudo docker system prune --all`


## POSTMAN Collection

Download the postman collection from [/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)
