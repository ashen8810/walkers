# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/requirements.txt


# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y default-jre python3-pip && \
    pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --timeout=120 -U pip && \
    pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --timeout=120 -r requirements.txt
    
# RUN  pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org databricks-connect==10.4.*

# Copy the current directory contents into the container at /app
COPY . /app


# Install OpenJDK-11
#RUN apt-get update && \
#    apt-get install -y openjdk-11-jdk && \
#    apt-get clean;
#
## Set environment variables
#ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
#ENV PYTHONUNBUFFERED=1

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run"]