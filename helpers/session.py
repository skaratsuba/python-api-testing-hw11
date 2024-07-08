import requests
from dotenv import load_dotenv
import os
load_dotenv()
class Session(requests.Session):
    def __init__(self, base_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        if self.base_url:
            url = self.base_url + url
        headers = kwargs.get('headers', {})
        headers['Authorization'] = os.getenv('TOKEN')
        kwargs['headers'] = headers
        return super().request(method, url, *args, **kwargs)
