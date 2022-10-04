import logging
import os
from time import sleep
from dotenv import load_dotenv
from cp4s.components.UDI import UDI

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

load_dotenv()


def main():
    udi = UDI(
        cp4s_url=os.getenv('CP4S_URL'),
        cp4s_api_user=os.getenv('CP4S_API_KEY'),
        cp4s_api_secret=os.getenv('CP4S_API_SECRET'),
        skip_ssl_verify=True
    )

    max_retries = 10
    retry_count = 0

    initial_query = udi.post_udi_query(
        query="[ipv4-addr:value = '10.45.1.1']",
        configuration_ids=None
    )

    if initial_query:
        query_id = initial_query['id']

        while True:
            query_status = udi.get_udi_query_status(query_id)
            if query_status and query_status.get('is_complete'):
                break
            elif retry_count > max_retries:
                logging.error("Query timed out")
                return
            else:
                retry_count += 1
                sleep(5)

        for page_id in query_status.get('pages', []):
            query_result = udi.get_udi_query_result(query_id, page_id)
            if query_result:
                logging.info(query_result)
            else:
                logging.error("Failed to retrieve query result")
                return


if __name__ == "__main__":
    main()
