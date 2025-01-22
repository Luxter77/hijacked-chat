# Use a lightweight Python image as the base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY chat /app/chat

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && pip install --upgrade pip \
    && pip install gunicorn flask mistletoe bleach bleach-allowlist \
    && apt-get remove -y gcc \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Make the run script executable
RUN chmod +x /app/chat/run_chat_api.sh

# Expose the port used by Gunicorn
EXPOSE 18052

# Command to run the application
CMD ["/app/chat/run_chat_api.sh"]
