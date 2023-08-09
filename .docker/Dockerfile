FROM odoo:16

ARG PROJECT_ROOT_PATH=.
ARG PROJECT_PKG_PATH=/home/odoo/osut
ARG PROJECT_ADDONS_PATH=/mnt/extra-addons
ARG CHROME_DEB_PATH=/var/cache/apt/archives/google-chrome.deb

USER root

RUN apt update;  \
    curl -o  ${CHROME_DEB_PATH} https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; \
    apt install -y ${CHROME_DEB_PATH}

COPY --chown=odoo:odoo ${PROJECT_ROOT_PATH} ${PROJECT_PKG_PATH}
COPY --chown=odoo:odoo ${PROJECT_ROOT_PATH}/tests_odoo ${PROJECT_ADDONS_PATH}

RUN pip install ${PROJECT_PKG_PATH}

USER odoo
