import socket
import ssl
import threading
from .utils import logger, metrics
from .protocol import ProtocolHandler
from .models import init_db

class SMTPXServer:
    def __init__(self, host='0.0.0.0', port=925):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain('certs/server.crt', 'certs/server.key')
        self.Session = init_db()
        self.running = False

    def handle_client(self, conn, addr):
        metrics.active_connections.inc()
        try:
            session = self.Session()
            handler = ProtocolHandler(session)
            # ECDH key exchange here
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = handler.handle_command(data)
                conn.sendall(response.encode())
        except Exception as e:
            logger.error(f"Client error: {str(e)}")
        finally:
            metrics.active_connections.dec()
            conn.close()

    def start(self):
        self.running = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)
        logger.info(f"Server started on {self.host}:{self.port}")

        while self.running:
            try:
                conn, addr = sock.accept()
                ssl_conn = self.context.wrap_socket(conn, server_side=True)
                threading.Thread(target=self.handle_client, args=(ssl_conn, addr)).start()
            except Exception as e:
                if self.running:
                    logger.error(f"Accept error: {str(e)}")

    def stop(self):
        self.running = False
