# Use a Node 22 base image for the OpenClaw body
FROM node:22-bullseye

# Install Python 3 and other required system dependencies (ffmpeg for media, sqlite for memory)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Install pnpm for OpenClaw dependencies
RUN npm install -g pnpm@10.23.0

# Copy system_body first to cache Node dependency installation
COPY system_body/package.json ./system_body/
# If there's a lockfile, copy it too. We use a wildcard to avoid failing if it doesn't exist.
COPY system_body/pnpm-lock.yaml* ./system_body/
RUN cd system_body && pnpm install

# Copy Python requirements and install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Copy the rest of the application
COPY . .

# Expose the OpenClaw Gateway port
EXPOSE 18789

# Command to run the unified agent (Starts Body + Brain)
CMD ["python3", "main.py"]
