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

    def get_udi_connections(self) -> Optional[Dict]:
        r = self.session.get(f"{self.base_url}/connections")
        if r.status_code == 200:
            return r.json()

        logger.error(f"Failed to retrieve UDI connections. "
                     f"error code = {r.status_code}")
        return None

    def post_udi_query(self, query, configuration_ids=None) -> Optional[Dict]:
        r = self.session.post(f"{self.base_url}/queries", json={
            "query": UDI._escape_query(query),
            "configuration_ids": ",".join(configuration_ids or []),
        })
        if r.status_code == 201:
            logger.info(f"UDI query posted successfully: '{query}'")
            return r.json()

        logger.warning(f"Failed to post UDI query: status_code={r.status_code}")
        return None

    def get_udi_query_status(self, query_id):
        r = self.session.get(f"{self.base_url}/queries/{query_id}")
        if r.status_code == 200:
            logger.debug(f"UDI query status: {r.json()}")
            return r.json()

        logger.warning(
            f"UDI retrieve query status failed: (status_code={r.status_code})"
        )
        return None

    def get_udi_query_result(self, query_id, page_id):
        r = self.session.get(
            f"{self.base_url}/queries/{query_id}/results/{page_id}",
            timeout=10,
        )
        if r.status_code == 200:
            return r.json()

        logger.warning(f"UDI retrieve query result failed: status_code={r.status_code}")
        return None

    def cancel_udi_query(self, query_id):
        r = self.session.post(
            f"{self.base_url}/queries/{query_id}/cancel",
        )
        if r.status_code == 200:
            return True
        logger.warning(f"UDI cancel query failed: status_code={r.status_code}")
        return False

    @staticmethod
    def _escape_query(query: str) -> str:
        if isinstance(query, str):
            if "\\" in query:
                query = query.replace("\\", "\\\\")
        return query
