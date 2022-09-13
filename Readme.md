# Clone solution

    git clone https://github.com/silashansen/epark_automation.git

## Push to ECR

    docker buildx build --platform linux/amd64 --push -t <region>.amazonaws.com/<imagename> .

*From here, you create a lambda function and point to this image.*

## Set epark credentials
Create the following environment variables in your function or environment:

    EPARK_USERNAME = <username>
    EPARK_PASSWORD = <password>

## Running locally

### Install dependencies
    pip3 install -r requirements.txt
**Make sure your pip is updated*:exclamation:

*It is known that some dependencies for running locally are missing in requirements.txt, since they are a part the base image used in the Dockerfile above - you may have to experiment*

### Run
    python3 app.py


