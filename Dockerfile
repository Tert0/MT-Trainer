FROM python:3-slim

COPY ./ /fastapi-app

WORKDIR /fastapi-app

RUN pip install --no-cache -r requirements.txt

CMD ["python", "-m", "app.main"]
