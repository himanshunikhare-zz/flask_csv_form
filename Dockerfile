FROM python:3.6-slim
RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev \

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip \
    pip install -r requirements.txt 

# Unit tests
RUN python -m unittest tests.py

EXPOSE 5000 
ENTRYPOINT [ "python" ] 
CMD [ "app.py" ] 
