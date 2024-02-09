# Use the official Ubuntu base image
FROM ubuntu:latest

# Update the package lists
RUN apt-get update -y && apt-get upgrade -y

# Install any necessary packages
# For example, to install curl:
# RUN apt-get install -y curl

# Any additional setup or configuration can go here

# Default command to execute when the container starts
CMD ["bash"]
