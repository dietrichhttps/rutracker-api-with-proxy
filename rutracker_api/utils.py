import urllib.parse

from bs4 import BeautifulSoup
from requests import Response

from rutracker_api.exceptions import AuthorizationException


def format_size(size_in_bytes):
    size_in_kilobytes = size_in_bytes / (1024)
    if size_in_kilobytes < 1024:
        return f"{round(size_in_kilobytes)} KB"
    size_in_megabytes = size_in_bytes / (1024 * 1024)
    if size_in_megabytes < 1024:
        return f"{round(size_in_megabytes, 1)} MB"
    size_in_gigabytes = size_in_bytes / (1024 * 1024 * 1024)
    if size_in_gigabytes < 1024:
        return f"{round(size_in_gigabytes, 2)} GB"
    size_in_terabytes = size_in_bytes / (1024 * 1024 * 1024 * 1024)
    return f"{round(size_in_terabytes, 3)} TB"


def generate_magnet(hash, tracker=None, title=None, url=None):
    params = {"xt": "urn:btih:" + hash}
    if tracker:
        params["tr"] = tracker
    if title:
        params["dn"] = title
    if url:
        params["as"] = url
    return "magnet:?" + urllib.parse.urlencode(params)


def is_autorized(response: Response, username: str) -> bool:
    soup = BeautifulSoup(response.text, 'html.parser')
    logged_in_username = soup.find('a', {'id': 'logged-in-username'})

    if 'profile.php?mode=register' in response.url:
        raise AuthorizationException('Ошибка авторизации. Проверьте логин и пароль.')
    if not logged_in_username or logged_in_username.text != username:
        raise AuthorizationException('Ошибка авторизации. Признаки успешного входа не найдены.')
    return True
