FROM python:3.11-bullseye
ADD requirements.txt /app
ADD main.py /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]