FROM python:3.10.5-alpine3.16
# LABEL maintainer="Operator2024 <work.pwnz+github@gmail.com>"
LABEL version="1.0.0"
ENV VER="0.1.2"
ENV INVMODE=""
ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \ 
  && apk add --no-cache ipmitool dmidecode gcc musl-dev jq && mkdir /workdir
COPY main.py  requirements.txt entrypoint.sh /workdir/
WORKDIR "/workdir"
RUN pip install -r requirements.txt && chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["$1", "$2"]
