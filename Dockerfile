FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD *.py /code/
RUN mkdir /code/dashboard
ADD dashboard/* /code/dashboard/
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt