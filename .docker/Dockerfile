ARG ODOO_VERSION
FROM odoo:$ODOO_VERSION

ARG PROJECT_ROOT_PATH=.
ARG PROJECT_PKG_PATH=/home/odoo/odoo-selenium
ARG PROJECT_ADDONS_PATH=/mnt/extra-addons
ARG CHROME_DEB_PATH=/var/cache/apt/archives/google-chrome.deb

USER root

RUN apt update;  \
    curl -o  ${CHROME_DEB_PATH} https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; \
    apt install -y ${CHROME_DEB_PATH}; \
    python3 -m pip install --upgrade pip coverage

COPY --chown=odoo:odoo ${PROJECT_ROOT_PATH}/.docker/odoo.conf /etc/odoo/odoo.conf
COPY --chown=odoo:odoo ${PROJECT_ROOT_PATH} ${PROJECT_PKG_PATH}
COPY --chown=odoo:odoo ${PROJECT_ROOT_PATH}/tests_odoo ${PROJECT_ADDONS_PATH}

RUN python3 -m pip install -e ${PROJECT_PKG_PATH}

COPY $PROJECT_ROOT_PATH/.docker/entrypoint.sh /


USER odoo
WORKDIR ${PROJECT_PKG_PATH}

ENV COVERAGE_HOME=${PROJECT_PKG_PATH}
ENV COVERAGE_RCFILE=${PROJECT_PKG_PATH}/.coveragerc
ENV COVERAGE_FILE=${PROJECT_PKG_PATH}/.coverage

ENTRYPOINT ["/entrypoint.sh"]
