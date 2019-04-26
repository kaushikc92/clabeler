FROM ubuntu:16.04
FROM python:3

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./src/ /code/
#RUN python manage.py makemigrations
#RUN python manage.py migrate

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
