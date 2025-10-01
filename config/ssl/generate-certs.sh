#!/bin/bash
# SSL Certificate Generation Script for ApexSigma Phase 2 Hardening
# Creates self-signed certificates for development and local production

set -e

echo "🔐 Generating SSL certificates for ApexSigma services..."

# Create CA private key
openssl genrsa -out ca-key.pem 4096

# Create CA certificate
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem -subj "/CN=ApexSigma-CA"

# Create server private key
openssl genrsa -out server-key.pem 4096

# Create certificate signing request
openssl req -subj "/CN=localhost" -sha256 -new -key server-key.pem -out server.csr

# Create extensions file for server certificate
cat > server-extfile.cnf <<EOF
subjectAltName = DNS:localhost,DNS:*.localhost,IP:127.0.0.1,IP:172.26.0.0/16
extendedKeyUsage = serverAuth
EOF

# Generate server certificate
openssl x509 -req -days 365 -in server.csr -CA ca.pem -CAkey ca-key.pem -out server-cert.pem -extensions v3_req -extfile server-extfile.cnf -CAcreateserial

# Create client private key
openssl genrsa -out client-key.pem 4096

# Create client certificate signing request
openssl req -subj "/CN=apexsigma-client" -new -key client-key.pem -out client.csr

# Create extensions file for client certificate
echo extendedKeyUsage = clientAuth > client-extfile.cnf

# Generate client certificate
openssl x509 -req -days 365 -in client.csr -CA ca.pem -CAkey ca-key.pem -out client-cert.pem -extfile client-extfile.cnf -CAcreateserial

# Clean up
rm server.csr client.csr server-extfile.cnf client-extfile.cnf

# Set appropriate permissions
chmod 400 ca-key.pem server-key.pem client-key.pem
chmod 444 ca.pem server-cert.pem client-cert.pem

echo "✅ SSL certificates generated successfully!"
echo "📁 Files created:"
echo "   - ca.pem (CA certificate)"
echo "   - ca-key.pem (CA private key)"
echo "   - server-cert.pem (Server certificate)"
echo "   - server-key.pem (Server private key)"
echo "   - client-cert.pem (Client certificate)"
echo "   - client-key.pem (Client private key)"
