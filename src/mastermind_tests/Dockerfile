FROM python:3

ARG tests

WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ${tests} ${tests}/

WORKDIR ${tests}
ENTRYPOINT [ "python","tests_integration.py" ]