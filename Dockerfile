FROM python:3.8-alpine3.13

RUN apk add --no-cache build-base && pip install pipenv

RUN adduser -D user
RUN mkdir -p /usr/src/app && chown user:user /usr/src/app
WORKDIR /usr/src/app
USER user

COPY requirements.txt .
COPY Pipfile* ./
RUN  pipenv install --deploy --ignore-pipfile

COPY . .

CMD ["pipenv", "run", "bot"]
