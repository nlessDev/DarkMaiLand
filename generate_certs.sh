#!/bin/bash
set -euo pipefail

CERT_DIR="certs"
DAYS=365
EC_CURVE="secp521r1"

mkdir -p "$CERT_DIR"

# Generate CA
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:"$EC_CURVE" \
  -days "$DAYS" -nodes \
  -keyout "$CERT_DIR/ca.key" \
  -out "$CERT_DIR/ca.crt" \
  -subj "/CN=SMTPX Root CA"

# Generate server cert
openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:"$EC_CURVE" \
  -nodes -keyout "$CERT_DIR/server.key" \
  -out "$CERT_DIR/server.csr" \
  -subj "/CN=smtpx-server"

openssl x509 -req -in "$CERT_DIR/server.csr" \
  -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" -CAcreateserial \
  -out "$CERT_DIR/server.crt" -days "$DAYS" \
  -extfile <(echo "subjectAltName=DNS:localhost,DNS:smtpx")

# Set permissions
chmod 600 "$CERT_DIR"/*
chmod 644 "$CERT_DIR/ca.crt" "$CERT_DIR/server.crt"

echo "Certificates generated in $CERT_DIR/"
