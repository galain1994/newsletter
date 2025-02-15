FROM python:3.11-slim-bullseye
LABEL maintainer="galain1994@gmail.com"

ENV LANG=C.UTF-8
ENV TZ=Asia/Shanghai
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r /tmp/requirements.txt

COPY ./src /workspace/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
