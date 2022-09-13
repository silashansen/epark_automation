FROM umihico/aws-lambda-selenium-python:latest

# Install the function's dependencies using file requirements.txt
# from your project folder.

#docker buildx build --platform linux/amd64 --push 

COPY requirements.txt  .
#RUN  python3 -m pip install --upgrade pip
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ] 