# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

COPY ./requirements.txt /app/requirements.txt
# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app


# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["qbit.py" ]


