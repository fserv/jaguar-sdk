FROM ubuntu:latest

ENV DOCKER_CONTAINER yes
ENV HOME /home/jaguar
RUN mkdir -p $HOME/jaguar

# Set the working directory inside the container
WORKDIR /workdir

# External program can connect to the port inside container
EXPOSE 8888

# Copy all files from the host's app directory to the container's directory
COPY ./releasedir /workdir

# Make the installation script executable
RUN chmod +x /workdir/install.sh

# Run the installation script in the container
RUN /workdir/install.sh

# Run the installation script inside the container
CMD ["/home/jaguar/jaguar/bin/jaguarstart"]
