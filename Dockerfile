FROM python:3.12

RUN apt-get update
RUN apt-get install -y --no-install-recommends make build-essential libsnappy1v5 libsnappy-dev 

# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install --no-cache-dir --upgrade gunicorn
COPY . /app
CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:80", "wsgi:app"]
