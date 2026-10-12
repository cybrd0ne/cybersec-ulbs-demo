# Front door image. Base pinned by digest (nginx:1.27-alpine), so Trivy and the build
# see exactly what shipped. Rebuilt in CI as frontdoor:ci and scanned before merge.
FROM nginx@sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10

COPY frontdoor.conf /etc/nginx/conf.d/default.conf

EXPOSE 8443

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget --no-verbose --tries=1 --no-check-certificate https://localhost:8443/ -O /dev/null || exit 1
