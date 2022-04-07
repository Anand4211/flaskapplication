FROM python
WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install -r requiremnets.txt
COPY . /code/

