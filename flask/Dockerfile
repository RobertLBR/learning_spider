FROM python:3.10
WORKDIR /usr/app/src
ADD weather_api.py ./
RUN pip install -i https://pypi.mirrors.ustc.edu.cn/simple flask bs4 requests lxml
CMD ["python3","weather_api.py"]