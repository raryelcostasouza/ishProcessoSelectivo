#Using official python docker image with Debian Bullseye slim version
FROM python:3.10.5-slim-bullseye

# Installing packages
RUN apt update && apt upgrade -y
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY safelabs ./safelabs

# Install API dependencies
RUN pipenv install

# Start app
EXPOSE 5000
ENTRYPOINT ["/bin/bash", "-c", "/usr/src/app/bootstrap.sh"]
