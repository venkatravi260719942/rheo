# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install pytest

# Define environment variable
ENV AWS_REGION=us-west-2

# Run app.py when the container launches
CMD ["python", "app.py"]
