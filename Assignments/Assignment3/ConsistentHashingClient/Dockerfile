FROM python:2.7
MAINTAINER Akshay Sonvane "akshay.sonvane93@gmail.com"
ADD . /code
COPY . /code
WORKDIR /code
EXPOSE 9000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
