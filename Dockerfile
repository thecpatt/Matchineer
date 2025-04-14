    # Use an official Python runtime as a parent image
    FROM python:3.12.5-slim

    # Set the working directory in the container
    WORKDIR /Senior_Project

    # Copy the requirements file into the container
    COPY requirements.txt .

    # Install any dependencies
    RUN apt-get update
    RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config
    RUN pip install -r requirements.txt

    # Copy the application code into the container
    COPY . .

    # Expose the port the app runs on
    EXPOSE 5000

    # Set environment variables (optional, but recommended)
    ENV FLASK_APP=app.py

    # Run the command to start the Flask app
    CMD ["flask", "run"]