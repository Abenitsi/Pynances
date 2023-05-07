FROM python:3.11

WORKDIR /app

COPY etc/requirements.txt /app/etc/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/erc/requirements.txt

COPY ../src /app/src

# Define an entrypoint
