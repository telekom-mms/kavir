FROM python:3.14

LABEL org.opencontainers.image.authors="I-Am-hehu" \
    org.opencontainers.image.base.name="python" \
    org.opencontainers.image.created="2026-01-05T11:00:00Z" \
    org.opencontainers.image.description="kavirs html-report-builder is a python script that uses kavirs csv files to build a html report (static html file)." \
    org.opencontainers.image.documentation="https://github.com/telekom-mms/kavir" \
    org.opencontainers.image.source="https://github.com/telekom-mms/kavir" \
    org.opencontainers.image.title="kavir-html-report-builder" \
    org.opencontainers.image.url="https://github.com/telekom-mms/kavir" \
    org.opencontainers.image.vendor="Deutsche Telekom MMS GmbH" \
    org.opencontainers.image.version="1.0.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    jq \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/kavir-html-report-builder
RUN mkdir /etc/kavir-html-report-builder

COPY ./docker/entrypoint.bash /opt/kavir-html-report-builder/entrypoint.bash
RUN chmod +x /opt/kavir-html-report-builder/entrypoint.bash

COPY ./src/main.py /opt/kavir-html-report-builder/main.py
COPY ./src/requirements.txt /opt/kavir-html-report-builder/requirements.txt
RUN pip3 install -r /opt/kavir-html-report-builder/requirements.txt

# templates
RUN mkdir /etc/kavir-html-report-builder/templates
COPY ./src/templates/simple.html.j2 /etc/kavir-html-report-builder/templates/simple.html.j2
# styles
RUN mkdir /etc/kavir-html-report-builder/styles
COPY ./src/styles/simple.css /etc/kavir-html-report-builder/styles/simple.css
COPY ./src/styles/tech.css /etc/kavir-html-report-builder/styles/tech.css

ENTRYPOINT ["/opt/kavir-html-report-builder/entrypoint.bash"]
