# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install uv for faster dependency installation
RUN pip install uv

# Install dependencies using uv
RUN uv pip install -e .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command when the container launches
ENTRYPOINT ["python", "-m", "markdown_notion"] 