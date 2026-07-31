# Use an official lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code into the container
COPY . .

# Expose port 5000 (the port Flask runs on inside the container)
EXPOSE 5000

# Specify the command to run the application
CMD ["python", "app.py"]
