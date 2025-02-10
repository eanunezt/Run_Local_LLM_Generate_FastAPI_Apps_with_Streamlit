#!/bin/bash

echo "Starting Ollama in the background..."
ollama serve &

# Wait for Ollama to be ready
until curl -s http://localhost:11434/api/tags > /dev/null; do
  echo "Waiting for Ollama to start..."
  sleep 2
done

echo "Installing models..."
ollama pull mistral
#ollama pull qwen2.5
#ollama pull deepseekcoder

echo "Models installed successfully."

# Keep Ollama running in the foreground
wait
