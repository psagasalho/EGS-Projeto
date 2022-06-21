FROM python:3.6-slim

ENV PROJECT_ROOT /app
ENV PYTHONUNBUFFERED=1
WORKDIR $PROJECT_ROOT

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000

#CMD gunicorn video_sharing.wsgi.application --bind 0.0.0.0:8000

