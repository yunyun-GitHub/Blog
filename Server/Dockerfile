FROM python:3.12-alpine
WORKDIR /Server/
COPY . /Server/
# 添加这一行解决Alpine版本安装python第三方库错误
RUN apk add --no-cache mariadb-connector-c-dev build-base libjpeg-turbo-dev zlib-dev libwebp-dev
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8000