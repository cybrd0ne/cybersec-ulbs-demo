# Front door image. Base pinned by digest (nginx:1.30.5-alpine), so Trivy and the build
# see exactly what shipped. Rebuilt in CI as frontdoor:ci and scanned before merge.
# A pinned digest does not age well: bump it when Trivy or Dependabot reports a fix.
FROM nginx:1.31.0-alpine@sha256:2f07d83bf561b506400dc183b1b2003803e39efbd22451f848adaba14d28c7c7

# Pull Alpine security fixes that landed after the base image was built. The base stays
# pinned; only patched distro packages change, and the Trivy gate checks the result (R-06).
RUN apk upgrade --no-cache

COPY frontdoor.conf /etc/nginx/conf.d/default.conf

EXPOSE 8443

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD ["sh", "-c", "wget --no-verbose --tries=1 --no-check-certificate https://localhost:8443/ -O /dev/null || exit 1"]
