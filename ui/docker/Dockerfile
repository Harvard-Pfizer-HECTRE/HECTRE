
# For Development

# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install Angular CLI globally
RUN npm install -g @angular/cli@17.3.5

# Install any needed packages specified in package.json
RUN npm install

# Make port 4200 available to the world outside this container
EXPOSE 4200

# Run ng serve when the container launches
CMD ["ng", "serve", "--host", "0.0.0.0", "--port", "4200"]