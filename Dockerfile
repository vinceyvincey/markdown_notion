# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install uv for faster dependency installation
RUN pip install uv

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies using uv
RUN uv sync

# Run the command when the container launches
ENTRYPOINT ["python", "-m", "markdown_notion"] 