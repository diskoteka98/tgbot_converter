FROM python:3.12

WORKDIR /app

COPY django_telegrambot_converter/requirements.txt /app

RUN pip install --no-cache-dir --upgrade pip setuptools

RUN pip install --no-cache-dir -r requirements.txt

COPY django_telegrambot_converter /app

# """new"""
EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]


