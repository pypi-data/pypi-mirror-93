import hashlib
import hmac
import json
import time
import logging
from base64 import b64decode, b64encode
from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from jwt import PyJWT

from coin_sdk.common.config import Config


class SecurityService:

    def __init__(self, config: Config):
        self._config = config
        self.jwt = PyJWT()
        self.expires_after = 30
        self.not_before = 30
        self.private_key = None
        self.shared_key = None
        self.now = None
        self.expires_at = None
        self.token = None
        self.private_key = self.load_pem(
            self._config.private_key_mem if self._config.private_key_mem else self.load_private_key()
        )
        self.shared_key = bytes(self._config.shared_key, 'utf-8') if self._config.shared_key \
            else self.load_shared_key(self.private_key)
        self.generate_token()

    def load_private_key(self, filename=None):
        filename = filename or self._config.private_key_file
        with open(filename, 'rb') as f:
            private_key_pem = f.read()
        return private_key_pem

    @staticmethod
    def load_pem(private_key_pem):
        return load_pem_private_key(private_key_pem, password=None, backend=default_backend())

    def load_shared_key(self, private_key,
                        filename=None):
        filename = filename or self._config.hmac_secret
        encrypted_key = None
        with open(filename, 'rb') as f:
            encrypted_key = b64decode(f.read())
        return private_key.decrypt(encrypted_key, padding.PKCS1v15())

    def generate_token(self):
        self.now = int(time.mktime(datetime.now().timetuple()))
        self.expires_at = self.now + self.expires_after
        message = {
            'iss': self._config.consumer_name,
            'nbf': self.now - self.not_before,
            'exp': self.now + self.expires_after
        }
        token = self.jwt.encode(message, self.private_key, 'RS256')
        self.token = token.decode('ascii')

    def token_has_expired(self):
        now = int(time.mktime(datetime.now().timetuple()))
        return self.token is None or now + 5 > self.now

    def get_token(self):
        if self.token_has_expired():
            self.generate_token()
        return self.token

    @staticmethod
    def httpdate():
        """Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.
        """
        now = datetime.utcnow()
        weekday = [
            'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][
            now.weekday()]
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                 'Oct', 'Nov', 'Dec'][now.month - 1]
        return '{}, {:02d} {} {:04d} {:02d}:{:02d}:{:02d} GMT'.format(
            weekday, now.day, month, now.year, now.hour, now.minute, now.second)

    @staticmethod
    def calculate_digest(msg):
        sha = hashlib.sha256()
        sha.update(msg)
        return b64encode(sha.digest())

    def create_digest(self, msg=b''):
        return f'SHA-256={self.calculate_digest(msg).decode("ascii")}'

    def generate_headers(self, url, method='get', request=None):
        uri = '/' + '/'.join(url.split('/')[3::]).split('?')[0]
        request_line = f'{method.upper()} {uri} HTTP/1.1'
        x_date = self.httpdate()
        digest = self.create_digest(json.dumps(request).encode() if request else b'')
        message = bytearray(f'digest: {digest}\nx-date: {x_date}\n{request_line}', 'ascii')
        logging.debug(self.shared_key)
        signature = hmac.new(self.shared_key, msg=message, digestmod=hashlib.sha256).digest()
        authorization = f'hmac username="{self._config.consumer_name}", algorithm="hmac-sha256", ' \
                        f'headers="digest x-date request-line", signature="{b64encode(signature).decode()}" '

        return {'digest': digest, 'x-date': x_date, 'authorization': str(authorization),
                'user-agent': 'coin-sdk-python-1.1.1'}

    def generate_jwt(self):
        return {'jwt': f'{self.get_token()}'}
