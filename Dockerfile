# Use an official Python runtime as a parent image with Python 3.10
FROM python:3.10-slim

# Set environment variables for Python and output buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Django
ENV DJANGO_SETTINGS_MODULE=django_note_taking_app.settings

# Run gunicorn to serve the Django application
CMD ["gunicorn", "django_note_taking_app.wsgi:application", "--bind", "0.0.0.0:8000"]
