#!/bin/bash
set -e

# Install dependencies
apt-get update
apt-get install -y python3 python3-pip openssl

# Setup virtual environment
python3 -m venv /opt/smtpx
source /opt/smtpx/bin/activate

# Install Python packages
pip install -r requirements.txt

# Generate certificates
mkdir -p certs
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:secp521r1 \
    -days 365 -nodes -keyout certs/server.key -out certs/server.crt \
    -subj "/CN=smtpx-server"

# Initialize database
python -c "from smtpx.models import init_db; init_db()"

# Set up systemd service
cat > /etc/systemd/system/smtpx.service <<EOF
[Unit]
Description=SMTPX Server
After=network.target

[Service]
User=smtpx
WorkingDirectory=/opt/smtpx
ExecStart=/opt/smtpx/bin/python -m smtpx.server
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable smtpx
systemctl start smtpx

echo "Deployment complete!"
