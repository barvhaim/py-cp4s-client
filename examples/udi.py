import logging
import os
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

    query_resp = udi.post_udi_query(
        query="[ipv4-addr:value = '10.45.1.1']",
        configuration_ids=['8c6931e8-cd60-4379-b34c-9f65030a7f33']
    )

    print(query_resp)


if __name__ == "__main__":
    main()
