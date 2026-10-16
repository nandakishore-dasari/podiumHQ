# ==============================================================================
# Stage 1: Node.js Asset Builder
# ==============================================================================
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ==============================================================================
# Stage 2: Hardened Non-Root Nginx Runtime
# ==============================================================================
FROM nginxinc/nginx-unprivileged:1.27-alpine AS runtime

LABEL org.opencontainers.image.title="PodiumHQ Frontend" \
      org.opencontainers.image.description="React + Vite Frontend for PodiumHQ Hackathon & Event Judging Platform" \
      org.opencontainers.image.vendor="PodiumHQ" \
      org.opencontainers.image.authors="nandakishore-dasari" \
      org.opencontainers.image.source="https://github.com/nandakishore-dasari/podiumHQ"

ENV BACKEND_HOST="backend" \
    BACKEND_PORT="8000"

# Copy built static assets from builder stage
COPY --from=builder --chown=101:101 /app/dist /usr/share/nginx/html

# Copy dynamic envsubst Nginx template
COPY --chown=101:101 nginx/default.conf.template /etc/nginx/templates/default.conf.template

USER 101

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://127.0.0.1:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
