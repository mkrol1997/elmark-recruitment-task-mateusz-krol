FROM python:3.11-alpine

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV DOTENV_FILE /app/elmark_warehouse/.env

WORKDIR /app
COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

COPY . .

EXPOSE 8000

CMD ["python", "./elmark_warehouse/manage.py", "runserver", "0.0.0.0:8000"]
