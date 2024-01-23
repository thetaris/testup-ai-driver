# Runtime image
FROM python:3
WORKDIR /opt/source

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src src

EXPOSE 5000
CMD ["python","src/app.py"]
