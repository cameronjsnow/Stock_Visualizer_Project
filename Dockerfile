# Use an official Python runtime
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project directory to the working directory
COPY . .

# Expose the port on which the Flask app will run (default is 5000)
EXPOSE 5000

# Set the command to run the Flask application
CMD ["python", "app.py"]