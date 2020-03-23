FROM python:3.8
RUN pip install pipenv
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system

COPY etl.py .
CMD [ "python", "-u", "etl.py" ]