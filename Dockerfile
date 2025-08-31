FROM ubuntu:22.04

# Add your desired configurations here, for example:
# RUN apt-get update && apt-get install -y ...

# Example: Install some useful tools
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    vim \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Set the default command to bash (or your preferred shell)
CMD ["bash"]