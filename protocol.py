import struct
from email.parser import BytesParser
from .utils import logger, metrics
from .exceptions import ProtocolError
from .spam_filter import SpamFilter

class ProtocolHandler:
    def __init__(self, session):
        self.session = session
        self.spam_filter = SpamFilter()
        self.current_message = None
        
    def handle_command(self, command, data):
        try:
            handler = getattr(self, f'handle_{command.lower()}', None)
            if not handler:
                raise ProtocolError(500, 'Unknown command')
            return handler(data)
        except Exception as e:
            logger.error(f"Command handling error: {str(e)}")
            metrics.errors.labels(type=e.__class__.__name__).inc()
            raise

    def handle_helo(self, data):
        return '220 Hello from SMTPX'

    def handle_mail(self, data):
        self.current_message = {'from': data.decode().strip(), 'rcpts': [], 'data': b''}
        return '250 OK'

    def handle_rcpt(self, data):
        if not self.current_message:
            raise ProtocolError(503, 'Need MAIL command first')
        self.current_message['rcpts'].append(data.decode().strip())
        return '250 OK'

    def handle_data(self, data):
        try:
            msg = BytesParser().parsebytes(data)
            spam_score = self.spam_filter.predict(msg.get_payload())
            if spam_score > 0.8:
                raise ProtocolError(550, 'Message rejected as spam')
            
            # Store message logic
            return '250 Message accepted'
        except Exception as e:
            logger.error(f"Data handling error: {str(e)}")
            raise ProtocolError(451, 'Local processing error')
