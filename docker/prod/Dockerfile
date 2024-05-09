FROM python:3.12.0

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && pip install -U poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry update --with prod

COPY ./docker/wait-for-it.sh /wait-for-it.sh
RUN sed -i 's/\r//' /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./docker/prod/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
