FROM python:3.10.5-alpine3.15
# LABEL maintainer="Operator2024 <work.pwnz+github@gmail.com>"
LABEL version="0.1.0"
ENV VER="0.1.0"
ENV INVMODE = ""
ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \ 
  && apk add --no-cache ipmitool dmidecode gcc musl-dev jq && mkdir /workdir
COPY main.py /workdir
COPY requirements.txt /workdir
WORKDIR "/workdir"
# RUN make -f Makefile build && chmod +x drive_scanner
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
CMD ["sh", "-c","python main.py -T \"$INVMODE\" | jq"]
