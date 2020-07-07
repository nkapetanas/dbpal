FROM python:3

# Set environment variables
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /

# Install dependencies.
RUN pip install -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code


RUN apt-get update
#RUN apt-get install python3-dev default-libmysqlclient-dev  -y
#RUN pip3 install mysqlclient
#RUN pip3 install PyMySQL

# Copy project code.
COPY . /code/

EXPOSE 8080

CMD ["uwsgi", "--http", ":8080", "--ini", "./uwsgi/uwsgi.ini"]
