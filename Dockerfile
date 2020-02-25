FROM python:3.6

WORKDIR /app
ENV PYTHONUNBUFFERED=0
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# EXPOSE 8001

# CMD ["python","manage.py", "runserver", "0.0.0.0:8001"]
