FROM python:3.9

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./verby /code/verby
COPY web.py /code/

CMD ["fastapi", "run", "web.py", "--port", "80"]
