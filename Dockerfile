FROM python:3.13-alpine

LABEL org.opencontainers.image.created="%%CREATED%%" \
      org.opencontainers.image.authors="nic.cheneweth@thoughtworks.com" \
      org.opencontainers.image.documentation="https://github.com/twplatformlabs/hello-restful" \
      org.opencontainers.image.source="https://github.com/twplatformlabs/hello-restful" \
      org.opencontainers.image.url="https://github.com/twplatformlabs/hello-restful" \
      org.opencontainers.image.version="%%VERSION%%" \
      org.opencontainers.image.vendor="ThoughtWorks, Inc." \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.title="hello-restful" \
      org.opencontainers.image.description="Lightweight API providing request and response endpoints" \
      org.opencontainers.image.base.name="%%BASE%%"

ENV MUSL_LOCPATH=/usr/share/i18n/locales/musl \
    LANG="C.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    PATH="/home/hello/.local/bin:${PATH}"

# hadolint ignore=DL3003
RUN apk add --no-cache \
        libintl=0.24.1-r0 \
        openssl=3.5.2-r0 && \
    apk --no-cache add --virtual build-dependencies \
        cmake==3.31.7-r1 \
        make==4.4.1-r3 \
        musl==1.2.5-r10 \
        musl-dev==1.2.5-r10 \
        musl-utils==1.2.5-r10 \
        gcc==14.2.0-r6 \
        gettext-dev==0.24.1-r0 && \
    wget -q https://gitlab.com/rilian-la-te/musl-locales/-/archive/master/musl-locales-master.zip && \
    unzip musl-locales-master.zip && cd musl-locales-master && \
    cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && \
    make && make install && \
    cd .. && rm -r musl-locales-master && \
    adduser -D hello && \
    apk del build-dependencies

WORKDIR /opt/app
COPY api/ api/
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && chmod -R 777 /opt/app

ENTRYPOINT ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "8000"]
