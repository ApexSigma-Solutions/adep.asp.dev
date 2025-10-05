#!/bin/sh
# Entrypoint script for ApexSigma SSL Proxy
# Generates certificates if they don't exist, then starts nginx

set -e

echo "🔐 Checking SSL certificates for ApexSigma SSL Proxy..."

# Generate certificates if they don't exist
if [ ! -f /etc/ssl/certs/server-cert.pem ] || [ ! -f /etc/ssl/private/server-key.pem ]; then
    echo "📜 Generating SSL certificates..."

    # Create CA private key
    openssl genrsa -out /etc/ssl/ca-key.pem 4096

    # Create CA certificate
    openssl req -new -x509 -days 365 -key /etc/ssl/ca-key.pem -sha256 -out /etc/ssl/certs/ca.pem -subj "/CN=ApexSigma-CA"

    # Create server private key
    openssl genrsa -out /etc/ssl/private/server-key.pem 4096

    # Create certificate signing request
    openssl req -subj "/CN=localhost" -sha256 -new -key /etc/ssl/private/server-key.pem -out /etc/ssl/server.csr

    # Create extensions file for server certificate
    cat > /etc/ssl/server-extfile.cnf <<EOF
subjectAltName = DNS:localhost,DNS:*.localhost,IP:127.0.0.1
extendedKeyUsage = serverAuth
EOF

    # Generate server certificate
    openssl x509 -req -days 365 -in /etc/ssl/server.csr -CA /etc/ssl/certs/ca.pem -CAkey /etc/ssl/ca-key.pem -out /etc/ssl/certs/server-cert.pem -extfile /etc/ssl/server-extfile.cnf -CAcreateserial

    # Clean up
    rm /etc/ssl/server.csr /etc/ssl/server-extfile.cnf

    # Set appropriate permissions
    chmod 400 /etc/ssl/ca-key.pem /etc/ssl/private/server-key.pem
    chmod 444 /etc/ssl/certs/ca.pem /etc/ssl/certs/server-cert.pem

    echo "✅ SSL certificates generated and installed"
else
    echo "✅ SSL certificates already exist, skipping generation"
fi

# Start nginx
echo "🚀 Starting Nginx SSL Proxy..."
exec nginx -g "daemon off;"