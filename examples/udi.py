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

    configs = udi.get_udi_configurations()
    print(configs)


if __name__ == "__main__":
    main()
