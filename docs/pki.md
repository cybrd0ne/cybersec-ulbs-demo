# PKI for the front door

A single root CA issues the leaf certificate the nginx front door serves. The root CA is
the one trust anchor every later service uses. The root private key never enters the
repository, and the generated leaf material lands in `pki/`, which is gitignored.

## With step-ca (smallstep)

```
# One-time root CA on this machine
step ca init --name "Lab Root" --dns localhost --address 127.0.0.1:9000 \
  --provisioner admin --deployment-type standalone

# Leaf certificate for the front door, written into pki/
mkdir -p pki
step ca certificate frontdoor.lab pki/frontdoor.crt pki/frontdoor.key \
  --ca-url https://127.0.0.1:9000 --root "$(step path)/certs/root_ca.crt"
```

## OpenSSL fallback

If smallstep is not installed, a root CA plus one leaf is enough for the demo:

```
mkdir -p pki && cd pki
openssl req -x509 -newkey rsa:4096 -nodes -keyout root_ca.key -out root_ca.crt \
  -days 365 -subj "/CN=Lab Root"
openssl req -newkey rsa:2048 -nodes -keyout frontdoor.key -out frontdoor.csr \
  -subj "/CN=frontdoor.lab"
openssl x509 -req -in frontdoor.csr -CA root_ca.crt -CAkey root_ca.key \
  -CAcreateserial -out frontdoor.crt -days 90 \
  -extfile <(printf "subjectAltName=DNS:localhost,DNS:frontdoor.lab")
```

## Wiring it in

`compose.yaml` mounts `pki/frontdoor.crt` and `pki/frontdoor.key` into the front door
read-only. Bring the stack up and open `https://localhost:${FRONTDOOR_HTTPS_PORT}` to see
the chain. Trust `pki/root_ca.crt` in your browser or client to clear the warning.

`pki/` and every `*.key` are gitignored (R-02). `root_ca.key` is the one file that must
never leave the machine.
