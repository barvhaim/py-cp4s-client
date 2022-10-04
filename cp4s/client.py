import requests
import logging

logger = logging.getLogger('cp4s.client')


class CP4S:
    def __init__(self, cp4s_url=None,
                 cp4s_api_user=None,
                 cp4s_api_secret=None,
                 skip_ssl_verify=False):
        self.cp4s_url = cp4s_url
        self.cp4s_api_user = cp4s_api_user
        self.cp4s_api_secret = cp4s_api_secret
        self.skip_ssl_verify = skip_ssl_verify
        self.session = self._setup_session()

    def _setup_session(self):
        session = requests.Session()
        session.auth = (self.cp4s_api_user, self.cp4s_api_secret)
        session.verify = not self.skip_ssl_verify
        session.headers.update({'Content-Type': 'application/json'})
        return session




