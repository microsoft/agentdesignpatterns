FROM mcr.microsoft.com/devcontainers/base:bookworm

# Configure npm to use Microsoft CFS-protected internal feed (corporate policy blocks registry.npmjs.org)
ENV npm_config_registry=https://packagefeedproxy.microsoft.io/npm/
RUN echo "registry=https://packagefeedproxy.microsoft.io/npm/" > /etc/npmrc

# Configure pip to use the Microsoft CFS-protected internal feed
ENV PIP_INDEX_URL=https://packagefeedproxy.microsoft.io/pypi/simple