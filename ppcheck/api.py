from functools import lru_cache

import requests

from ppcheck.constants import API_URL


class ApiManager:
    api_url = API_URL

    @classmethod
    @lru_cache(maxsize=128)
    def get_password_results(cls, hash: str) -> int:
        hash = hash.upper()
        request_result = requests.get(f"{cls.api_url}/{hash[0:5]}")
        if hash[5:] in request_result.text:
            for hash_result in request_result.text.split():
                if hash[5:] in hash_result:
                    return int(hash_result.split(":")[1])
        return 0
