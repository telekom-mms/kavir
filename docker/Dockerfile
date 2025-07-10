FROM bitnami/kubectl:1.33

LABEL org.opencontainers.image.authors="I-Am-hehu" \
    org.opencontainers.image.base.name="bitnami/kubectl" \
    org.opencontainers.image.created="2025-07-09T16:00:00Z" \
    org.opencontainers.image.description="kavir forwards information about applications in a kubernetes cluster to a git repository. This way software and stakeholders without access to the kubernetes cluster can still see the image names and versions that are used by the applications in the cluster." \
    org.opencontainers.image.documentation="https://github.com/telekom-mms/kavir/tree/main" \
    org.opencontainers.image.source="https://github.com/telekom-mms/kavir/tree/main" \
    org.opencontainers.image.title="kavir" \
    org.opencontainers.image.url="https://github.com/telekom-mms/kavir/tree/main" \
    org.opencontainers.image.vendor="Deutsche Telekom MMS GmbH" \
    org.opencontainers.image.version="1.1.0"

COPY ./kavir.bash /opt/kavir.bash
ENTRYPOINT /bin/bash /opt/kavir.bash
