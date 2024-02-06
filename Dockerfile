# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Apply Django migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# create super 
# RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" 

# Expose the port django is running on
EXPOSE 8000

# Define the command to run your django project
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]