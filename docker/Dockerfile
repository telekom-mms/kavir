FROM debian:trixie-20250908-slim

LABEL org.opencontainers.image.authors="I-Am-hehu" \
    org.opencontainers.image.base.name="debian:trixie-20250908-slim" \
    org.opencontainers.image.created="2025-09-28T16:00:00Z" \
    org.opencontainers.image.description="kavir forwards information about applications in a kubernetes cluster to a git repository. This way software and stakeholders without access to the kubernetes cluster can still see the image names and versions that are used by the applications in the cluster." \
    org.opencontainers.image.documentation="https://github.com/telekom-mms/kavir" \
    org.opencontainers.image.source="https://github.com/telekom-mms/kavir" \
    org.opencontainers.image.title="kavir" \
    org.opencontainers.image.url="https://github.com/telekom-mms/kavir" \
    org.opencontainers.image.vendor="Deutsche Telekom MMS GmbH" \
    org.opencontainers.image.version="1.2.0"

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    git \
    && curl -LO "https://dl.k8s.io/v1.34.0/bin/linux/amd64/kubectl" && chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl \
    && apt-get clean

COPY ./kavir.bash /usr/local/bin/kavir.bash
RUN chmod +x /usr/local/bin/kavir.bash

RUN groupadd --gid 1001 kavir && \
    useradd --uid 1001 --gid 1001 kavir
USER 1001

ENTRYPOINT ["kavir.bash"]
