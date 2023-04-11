# Use an official Python runtime as a parent image
FROM python:3.10.4-slim-buster


# Set the working directory to /app
WORKDIR /moviezone_project

# Copy the requirements file into the container at /app
COPY requirements.txt /moviezone_project/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /moviezone_project/

# Set environment variable to ensure that Python output is sent straight to terminal
ENV PYTHONUNBUFFERED 1

# Expose port 8000 for the Django app to listen on
EXPOSE 8000

# Run the command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
