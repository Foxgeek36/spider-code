FROM baseimage
MAINTAINER dragon <shixl@fosun.com>
#WORKDIR ./wechattiangou
WORKDIR /app
copy ./wechattiangou/tiangou.py .
copy requirements.txt .
RUN apt-get update && apt-get install -y adb
RUN ["pip3","install","-r","requirements.txt"]
EXPOSE 5037
CMD python3 tiangou.py
