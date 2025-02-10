# Dockerfile for ollamasrv
FROM ollama/ollama:latest

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy init_models.sh script
COPY init_models.sh /app/init_models.sh

# Make the script executable
RUN chmod +x /app/init_models.sh

# Expose necessary ports
EXPOSE 11434
