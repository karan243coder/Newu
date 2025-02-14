# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Set the environment variable for the bot token
# (you can also set this using environment variables in Docker when running the container)
ENV BOT_TOKEN="7400491029:AAF5r3cfKWpP8aXjI683z3izeca1YLhGVXc"

# Expose any ports your bot may need (usually none for this kind of bot)
EXPOSE 8080

# Command to run the bot when the container starts
CMD ["python", "bot.py"]
