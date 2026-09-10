FROM mcr.microsoft.com/devcontainers/python:3.14-trixie

ARG USERNAME=qz
ARG USER_UID=1005
ARG USER_GID=1005

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd \
        --uid ${USER_UID} \
        --gid ${USER_GID} \
        --create-home \
        --shell /bin/bash \
        ${USERNAME} \
    && apt-get update \
    && apt-get install -y --no-install-recommends sudo \
    && echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME} \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && apt install -y git 

ENV DEVELOPMENT=true
RUN pip install --no-cache-dir django-npm-dev

WORKDIR /opt/quinzo
COPY . /opt/quinzo
COPY pyproject.toml .
RUN pip install -e .

RUN cd /opt/quinzo/src && npm install
RUN cd /opt/quinzo/src && cp node_modules/flowbite/dist/flowbite.min.js quinzo/static/quinzo/flowbite.min.js

USER ${USERNAME}