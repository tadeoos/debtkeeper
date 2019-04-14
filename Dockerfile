FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./backend /app
WORKDIR /app
RUN pip install -r /app/requirements.txt
