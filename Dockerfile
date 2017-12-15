FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD *.py /code/
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt