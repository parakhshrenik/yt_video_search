FROM python:3.8

ADD yt_crawler.py .
ADD __init__.py .
ADD Logs .
ADD logs.txt Logs

RUN pip install requests elasticsearch
CMD ["python", "./test.py", "WTC"]
