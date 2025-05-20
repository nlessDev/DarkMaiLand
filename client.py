import socket
import ssl
from .crypto import SMTPXCrypto
from email.mime.multipart import MIMEMultipart

class SMTPXClient:
    def __init__(self, server, port=925):
        self.server = server
        self.port = port
        self.crypto = SMTPXCrypto()
        self.conn = None

    def connect(self):
        sock = socket.create_connection((self.server, self.port))
        context = ssl.create_default_context()
        self.conn = context.wrap_socket(sock, server_hostname=self.server)
        # Perform ECDH key exchange here

    def send_mail(self, from_addr, to_addrs, msg_body, attachments=[]):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = ', '.join(to_addrs)
        msg.attach(msg_body)
        
        for att in attachments:
            msg.attach(att)
            
        encrypted = self.crypto.encrypt(msg.as_bytes())
        self.conn.sendall(encrypted)
        return self.conn.recv(1024)

    def disconnect(self):
        if self.conn:
            self.conn.close()
