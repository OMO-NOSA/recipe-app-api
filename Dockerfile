FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

# -- Install Application into container:
RUN  mkdir /app

WORKDIR /app

# -- copying project dependency
COPY requirements.txt requirements.txt

# -- Install dependencies:
RUN pip install -r requirements.txt

RUN adduser -D user

USER user
# -- Listening ports:
EXPOSE 8000
# -- Run Commands:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]