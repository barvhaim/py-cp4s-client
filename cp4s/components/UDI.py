import logging
from typing import Dict, Optional
import requests
from cp4s.client import CP4S

logger = logging.getLogger('cp4s.udi')


class UDI(CP4S):
    def __init__(self, cp4s_url=None,
                 cp4s_api_user=None,
                 cp4s_api_secret=None,
                 skip_ssl_verify=False
                 ):
        super().__init__(cp4s_url, cp4s_api_user, cp4s_api_secret, skip_ssl_verify)
        self.base_url = f'{self.cp4s_url}/api/uds/v3'

    def get_udi_configurations(self) -> Optional[Dict]:
        r = self.session.get(f"{self.base_url}/configurations")

        if r.status_code == 200:
            return r.json()

        logger.error(f"Failed to retrieve UDI configurations. "
                     f"error code = {r.status_code}")
        return None

