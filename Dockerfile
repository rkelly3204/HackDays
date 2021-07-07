FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
CMD ["NFL_Web.py"]

ENTRYPOINT ["python3"]
