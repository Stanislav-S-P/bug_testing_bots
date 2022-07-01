FROM python:3.8.10


COPY . /home/app/bug_report_bot
WORKDIR /home/app/bug_report_bot
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]