FROM python:3.8
ENV OBJECT_AI_REPO_PATH=/Object-AI POETRY_VERSION=1.1.13
RUN pip install "poetry==${POETRY_VERSION}"
WORKDIR /Object-AI/object_ai

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./object_ai ./object_ai
COPY ./setup.py ./
COPY ./env ./env
COPY ./tests ./tests

RUN pip install .

EXPOSE 5000
ENTRYPOINT ["python", "object_ai/app/application.py"]