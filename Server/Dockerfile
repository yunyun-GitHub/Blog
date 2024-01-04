FROM python:3.12-alpine
WORKDIR /Server/
COPY . /Server/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8000