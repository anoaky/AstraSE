FROM python:3.11-bullseye
WORKDIR /astra-se
COPY . .
RUN pip install .
CMD ["python3", "main.py"]