# Base image
FROM python:3.11-alpine3.17

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copies over project files
RUN mkdir /ntumods
WORKDIR /ntumods
COPY . .

# Setup django
WORKDIR /ntumods/backend
RUN pip install -r requirements.txt

# Build React app and copies static files to django
WORKDIR /ntumods/frontend
RUN apk add --update nodejs npm
RUN npm install --legacy-peer-deps
RUN npm run build
RUN cp -r build ../backend/

# Expose the Django app port
EXPOSE 8000

# Start the Django app
WORKDIR /ntumods/backend
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]