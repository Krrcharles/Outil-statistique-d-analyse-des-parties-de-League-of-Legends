FROM python:3.10.4

COPY . .

RUN pip install -r requirements.txt
CMD ["python", "/__main__.py"]