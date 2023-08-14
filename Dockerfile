FROM python:3.6.4-slim
MAINTAINER Giorgos Matzarapis "matzarapis@ceid.upatras.gr"
COPY src /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]
