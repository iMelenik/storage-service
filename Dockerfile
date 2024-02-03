FROM python:3.10-slim
WORKDIR /home/app

# send output straight to the container logs instead of buffering
ENV PYTHONUNBUFFERED 1
# Python won’t try to write .pyc files on the import of source modules.
ENV PYTHONDONTWRITEBYTECODE 1

# update pip and install pipenv
RUN pip install --upgrade pip

# install python packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . /home/app
