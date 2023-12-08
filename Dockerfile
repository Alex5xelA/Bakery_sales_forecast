FROM python:3.10.6-buster

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY bakerysales /bakerysales
COPY setup.py /setup.py
RUN pip install .

COPY Makefile /Makefile
RUN make reset_local_files

CMD uvicorn bakerysales.api.fast:app --host 0.0.0.0
