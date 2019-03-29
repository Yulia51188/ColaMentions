import requests
from dotenv import load_dotenv
import os
def main():
    load_dotenv()
    service_key = os.getenv("SERVICE_KEY")
    access_token = os.getenv("ACCESS_TOKEN")    
    vk_api_version = os.getenv("VERSION")


if __name__ == '__main__':
    main()
