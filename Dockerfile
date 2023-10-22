FROM python:3.10-alpine

RUN apk add py3-pip \
    && pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "flask", "--app", "./src/app.py", "--debug", "run", "--host=0.0.0.0"]