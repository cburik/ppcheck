import requests

from pwned_password_checker.constants import API_URL


def get_password_results(hash: str) -> int:
    request_result = requests.get(f"{API_URL}/{hash[0:5]}")
    print(request_result.text)
    if hash[5:] in request_result.text:
        for hash_result in request_result.text.split():
            if hash[5:] in hash_result:
                count = int(hash_result.split(":")[1])
    else:
        count = 0
    return count
