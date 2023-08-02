FROM python:3.8

WORKDIR /code
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENV HOME /home/walden2
RUN groupadd -g 1000 walden2
RUN useradd -u 1000 -g 1000 -m -d $HOME walden2

USER walden2

CMD ["python", "./script.py"]
