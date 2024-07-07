FROM python:3.11-bullseye
RUN mkdir -p /var/www/astra/app
RUN mkdir -p /var/www/astra/app/data
ADD requirements.txt /var/www/astra/app
ADD main.py /var/www/astra/app
WORKDIR /var/www/astra/app
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]