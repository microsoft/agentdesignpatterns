FROM mcr.microsoft.com/devcontainers/base:bookworm

# Configure npm to use Microsoft CFS-protected internal feed (corporate policy blocks registry.npmjs.org)
ENV npm_config_registry=https://packagefeedproxy.microsoft.io/npm/
RUN echo "registry=https://packagefeedproxy.microsoft.io/npm/" > /etc/npmrc

# Configure pip to use the Microsoft CFS-protected internal feed
ENV PIP_INDEX_URL=https://packagefeedproxy.microsoft.io/pypi/simple

# APM's native Linux binary requires glibc 2.38+, while Debian Bookworm provides 2.36.
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/apm \
    && /opt/apm/bin/pip install --no-cache-dir apm-cli \
    && ln -s /opt/apm/bin/apm /usr/local/bin/apm