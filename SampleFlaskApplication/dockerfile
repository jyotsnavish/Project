FROM rockylinux:9.1.20230215-minimal

# Install required packages for Flask
RUN microdnf install -y dnf
RUN dnf install -y python3 python3-pip

# Copy the Flask app into the container
COPY . /app

# Install the required packages for the Flask app
RUN pip3 install -r /app/requirements.txt

# Set the working directory
WORKDIR /app

# Expose the port used by the Flask app
EXPOSE 5000

# Start the Flask app
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]