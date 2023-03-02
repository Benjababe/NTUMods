# Base image
FROM python:3.11-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

# Set up the working directory for Django app
WORKDIR /backend

# Copy the requirements file
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire Django project folder to the container
COPY . .

# Set up the working directory for React app
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps

# Build the React app
RUN cd frontend && npm run build && cd ..

# Copy the build content to the Django app
RUN cp -r /frontend/build/ /backend/

# Expose the Django app port
EXPOSE 8000

# Start the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]