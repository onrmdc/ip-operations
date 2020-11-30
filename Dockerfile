FROM python:latest

WORKDIR /project
COPY ./ip-operations/requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5002:5000

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "--chdir", "/project", "app:app", "--reload", "--timeout", "900"]
