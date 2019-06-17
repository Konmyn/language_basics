FROM python:3.6.8-stretch
ADD pip.conf /etc/pip.conf
WORKDIR /app
ADD credentials.json .
ADD docker-registry-migrate-to-s3.py .
ADD requirements.txt .
RUN pip install -r /app/requirements.txt
CMD /app/docker-registry-migrate-to-s3.py
