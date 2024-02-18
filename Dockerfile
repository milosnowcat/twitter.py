FROM python:3.11

WORKDIR /src

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

RUN DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --noinput --username admin --email test@rahcode.com

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
