FROM python:3
 
# Install redact-pdf-tools
RUN apt-get update && apt-get -y install sudo
RUN sudo apt-get -y install imagemagick libimage-exiftool-perl python-stdeb python-all fakeroot build-essential ghostscript
RUN git clone https://github.com/micahflee/pdf-redact-tools.git && cd pdf-redact-tools && python2 setup.py install

# Create the group and user to be used in this container
RUN groupadd dorotogroup && useradd -m -g dorotogroup -s /bin/bash doroto
 
# Create the working directory (and set it as the working directory)
RUN mkdir -p /home/doroto/api
RUN mkdir -p /home/doroto/uploads
WORKDIR /home/doroto/api
 
COPY requirements.txt /home/doroto/api
RUN pip install -r requirements.txt
 
# Copy the source code into the container
COPY . /home/doroto/api
 
RUN chown -R doroto:dorotogroup /home/doroto
 
USER doroto