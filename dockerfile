# Use the official Python base image
FROM python:3.7.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Expose the port on which your Flask app will run (adjust if needed)
EXPOSE 5000

# Command to run your Flask app
CMD ["python", "app.py"]
