import pytest
from smtpx.protocol import ProtocolHandler
from smtpx.utils.exceptions import ProtocolError

class TestProtocol:
    @pytest.fixture
    def handler(self, mocker):
        mock_session = mocker.Mock()
        return ProtocolHandler(mock_session)

    def test_helo_command(self, handler):
        response = handler.handle_command('HELO', b'')
        assert response == '220 Hello from SMTPX'

    def test_mail_sequence(self, handler):
        handler.handle_command('MAIL', b'FROM:<user@example.com>')
        response = handler.handle_command('RCPT', b'TO:<recipient@example.com>')
        assert response == '250 OK'

    def test_invalid_command(self, handler):
        with pytest.raises(ProtocolError) as exc:
            handler.handle_command('INVALID', b'')
        assert exc.value.code == 500

    def test_data_without_recipient(self, handler):
        handler.handle_command('MAIL', b'FROM:<user@example.com>')
        with pytest.raises(ProtocolError) as exc:
            handler.handle_command('DATA', b'Test message')
        assert exc.value.code == 503
