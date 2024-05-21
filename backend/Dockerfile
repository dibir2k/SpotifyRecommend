# Use the official Python image as a base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

EXPOSE 5000
# Command to run the application

# Make the shell script executable
RUN chmod +x /app/start.sh

# Run the shell script
CMD ["./start.sh"]
# CMD ["waitress-serve", "--port=8000", "wsgi:app"]
# CMD ["python", "create_collection.py && wsgi.py"]
