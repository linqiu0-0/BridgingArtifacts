# Install the base requirements for the app.
FROM python:3.9.7-alpine

RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
# flask --app server --debug run
CMD ["flask", "--app", "server", "--debug", "run", "--host=0.0.0.0"]
EXPOSE 5000
