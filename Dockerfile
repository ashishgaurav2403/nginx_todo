FROM python:3.9-slim

WORKDIR /app

# Install Flask
RUN pip install Flask   

# Copy the application code to the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5006

# Command to run the Flask app
CMD ["python", "app.py"]