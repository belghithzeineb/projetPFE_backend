# Use the official Python image as the base image
FROM python:3.8

# Copy all the project files to the Docker image
COPY . /app

# Set the working directory to the root directory of the project
WORKDIR /app

# Install the required Python packages
RUN pip install -r requirements.txt

# Expose port 5000, which is the default port that Flask uses
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
