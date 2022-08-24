FROM python:3.9-slim-bullseye

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONBUFFERED=1

CMD ["uvicorn", "--port=8080", "--host=0.0.0.0", "--proxy-headers", "--forwarded-allow-ips=*", "--timeout-keep-alive=20", "ws_repro.main:app"]
