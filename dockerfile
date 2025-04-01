FROM python:3.12.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /main

COPY requirements.txt /main/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./app /main/app
COPY ./scripts /main/scripts

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
