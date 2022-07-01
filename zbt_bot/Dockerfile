FROM python:3.8.10

COPY . /home/app/zbt_bot
WORKDIR /home/app/zbt_bot
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]