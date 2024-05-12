# Use the official Python image for Python 3.12 as a base
FROM python:3.12-slim

# Copy the requirements file into the container
# COPY requirements.txt .

RUN pip install matplotlib

RUN pip install python-jose[cryptography]

RUN pip install fastapi[all]

RUN pip install sqlalchemy

RUN pip install pandas

RUN pip install python-multipart

RUN pip install passlib[bcrypt]

RUN pip install unicorn[standard]

RUN pip install cachetools

RUN pip install fastapi

RUN pip install mediapipe

RUN pip install opencv-python

RUN pip install numpy

RUN pip install pillow

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port on which your FastAPI application runs
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
