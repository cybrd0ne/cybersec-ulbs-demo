# Front door image. Base pinned by digest (nginx:1.30.5-alpine), so Trivy and the build
# see exactly what shipped. Rebuilt in CI as frontdoor:ci and scanned before merge.
# A pinned digest does not age well: bump it when Trivy or Dependabot reports a fix.
FROM nginx:1.31.7-alpine@sha256:892bb2152464f0c5d8972593a5f5afaf8054552580b699d95f8ff4af08c2d33d

# Pull Alpine security fixes that landed after the base image was built. The base stays
# pinned; only patched distro packages change, and the Trivy gate checks the result (R-06).
RUN apk upgrade --no-cache

COPY frontdoor.conf /etc/nginx/conf.d/default.conf

EXPOSE 8443

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD ["sh", "-c", "wget --no-verbose --tries=1 --no-check-certificate https://localhost:8443/ -O /dev/null || exit 1"]
