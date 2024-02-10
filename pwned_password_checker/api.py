import requests

from pwned_password_checker.constants import API_URL


class ApiManager:
    api_url = API_URL

    @classmethod
    def get_password_results(cls, hash: str) -> int:
        request_result = requests.get(f"{cls.api_url}/{hash[0:5]}")
        if hash[5:] in request_result.text:
            for hash_result in request_result.text.split():
                if hash[5:] in hash_result:
                    return int(hash_result.split(":")[1])
        return 0
