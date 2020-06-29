FROM python:3.8-alpine
# MenuRoma is the maintainer of the Project and image.
LABEL maintainer="MenuRoma"

# * Environment variable setup in docker image.

# Tells python to run in unbuffered mode, this allows python
# to print directly rather to hold in buffer
ENV PYTHONUNBUFFERED 1


# * Configuring the dependencies for the project

# Copies the python requirements.txt in local project to requirements.txt in docker image.
COPY ./requirements.txt /requirements.txt
# Running the python command to install all requirements in docker image.
RUN pip install -r /requirements.txt


# * Configuring the project directories.

# Creating a app (working directory) in docker image
RUN mkdir /app
# Setting the app directory as working directory in docker image.
WORKDIR /app
# Copying the contents of app directory in local project to the docker image.
COPY ./app /app


# * Configuring the authentications.

# Creating a user to run the applications only in docker image.
RUN adduser -D user
# Switching to the user
USER user
