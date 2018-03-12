FROM python:3.6.1
 
# Create the group and user to be used in this container
RUN groupadd dorotogroup && useradd -m -g dorotogroup -s /bin/bash doroto
 
# Create the working directory (and set it as the working directory)
RUN mkdir -p /home/doroto/api
WORKDIR /home/doroto/api
 
COPY requirements.txt /home/doroto/api
RUN pip install -r requirements.txt
 
# Copy the source code into the container
COPY . /home/doroto/api
 
RUN chown -R doroto:dorotogroup /home/doroto
 
USER doroto