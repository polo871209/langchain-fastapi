# Use an official Python runtime as the parent image
FROM python:3.11-slim

# Set the working directory in the docker image
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    libgeos-c1v5 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

# aws Bedrock spcific package
RUN python3 -m pip install boto3-1.28.21-py3-none-any.whl
RUN python3 -m pip install botocore-1.31.21-py3-none-any.whl

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]