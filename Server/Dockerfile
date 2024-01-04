FROM python:3.12-alpine
WORKDIR /Server/
COPY . /Server/
# 添加这一行解决Alpine版本安装mysqlclient错误
RUN apk add --no-cache mariadb-connector-c-dev build-base
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8000