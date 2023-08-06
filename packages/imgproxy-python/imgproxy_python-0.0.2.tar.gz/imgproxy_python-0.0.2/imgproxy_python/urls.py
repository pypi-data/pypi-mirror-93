import base64
import hashlib
import hmac
import textwrap
from urllib.parse import urljoin


class UrlGenerator:
    def __init__(self, url, config):
        self.url = url
        self.key = bytes.fromhex(config['imgproxy_key'])
        self.host = config['imgproxy_host']
        self.salt = bytes.fromhex(config['imgproxy_salt'])
        self.options = config['options']

    def prepare_options(self):
        if self.options.get('type', 'simple') == 'simple':
            self.options.setdefault('width', 0)
            self.options.setdefault('height', 0)
            self.options.setdefault('resize', 'fit')
            self.options.setdefault('gravity', 'ce')
            self.options.setdefault('enlarge', 0)
            self.options.setdefault('extension', '')
        else:
            raise NotImplementedError

    def generate_unsigned_url(self):
        self.prepare_options()
        encoded_url = base64.urlsafe_b64encode(self.url.encode()).rstrip(b"=").decode()
        # You can trim padding spaces to get good-looking url
        encoded_url = '/'.join(textwrap.wrap(encoded_url, 16))
        path = "/{resize}/{width}/{height}/{gravity}/{enlarge}/{encoded_url}{extension}".format(
            encoded_url=encoded_url,
            resize=self.options['resize'],
            width=self.options['width'],
            height=self.options['height'],
            gravity=self.options['gravity'],
            enlarge=self.options['enlarge'],
            extension=self.options['extension']
        )
        return path

    def generate_signed_url(self):
        unsigned_url = self.generate_unsigned_url().encode()
        digest = hmac.new(self.key, msg=self.salt + unsigned_url, digestmod=hashlib.sha256).digest()
        protection = base64.urlsafe_b64encode(digest).rstrip(b"=")
        url = b'/%s%s' % (
            protection,
            unsigned_url,
        )
        return url.decode()

    def get_full_signed_url(self):
        return urljoin(self.host, self.generate_signed_url())