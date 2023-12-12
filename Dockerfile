FROM python:3.10.6-buster
WORKDIR /prod

COPY requirements_prod.txt requirements.txt
COPY bakery_sales bakery_sales
COPY models models
COPY setup.py setup.py
COPY api api
COPY weights weights

RUN pip install --upgrade pip
RUN pip install -e .
RUN pip install fastapi uvicorn
RUN pip install python-multipart

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT