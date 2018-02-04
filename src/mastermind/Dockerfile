FROM tiangolo/uwsgi-nginx-flask:python3.6
ARG api
ARG tests

WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ${api} ${api}/
COPY ${tests} ${tests}/

RUN PYTHONPATH=${api} python -m src.mastermind_tests.tests

WORKDIR ${api}
ENTRYPOINT [ "python","api.py" ]