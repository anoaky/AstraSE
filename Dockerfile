FROM python:3.11-bullseye
WORKDIR /app
COPY . .
RUN pip install .
CMD ["python3", "main.py"]