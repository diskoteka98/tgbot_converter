FROM python:3.12

WORKDIR /app

COPY django_telegrambot_converter/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY django_telegrambot_converter /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]


