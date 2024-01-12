from dataclasses import dataclass
import hashlib
from urllib.parse import urlparse

import requests


TOKEN_SECRET = "vopfe2krtkmotr"
INPUT_FILE = "de_domains.csv"
BASE_URL = "https://jpad.labeloffice.com/json.php"


@dataclass
class APIResult:
    """
    The result of the API call. Contains the age at which the website is allowed to be accessed and whether it is allowed to be accessed.

    The result is returned as a JSON object by the jugendschutzprogramm.de API.
    """

    age: int  # the age at which the website is allowed to be accessed
    scope_url: str  # the url that was checked
    show: bool  # whether the website is allowed to be accessed
    cache: str  # whether the result was cached

    overrule: str
    type: str
    list: str
    cou: str
    urlcheck: str
    age_icon: str
    otf: str
    country: str
    age_issuer: str

    def __str__(self):
        return f"{self.scope_url} is available starting at age {self.age}."


class JugendschutzAPIClientException(Exception):
    """
    An exception that is raised when the API returns an error.
    """

    pass


class JugendschutzAPIClient:
    def __init__(self, base_url: str = BASE_URL, token_secret: str = TOKEN_SECRET):
        self.base_url = base_url
        self.token_secret = token_secret

    def __generate_api_token(self, url: str):
        """
        Generates an API token for the given url. The token is used to authenticate the request.
        The token is generated by md5-hashing the url together with a secret token and then appending the length of the url.
        The last 6 characters of the hash are returned.
        :param url: the url to generate the token for (e.g. "bild.de")
        :return: the last 6 characters of the hash
        """
        generated_hash = hashlib.md5((url + self.token_secret).encode()).hexdigest()
        generated_hash += str(len(url))
        return generated_hash[max(0, len(generated_hash) - 6) :]

    def check_url(self, url: str, age: int):
        """
        Checks whether the given url is allowed to be accessed by the given age.
        And returns also the minimum age at which the website is allowed to be accessed.

        Usage example:
        client = APIClient()
        print(client.check_url("bild.de", 16))
        >> *.bild.de/* is available starting at age 12.
        print(client.check_url("https://bild.de", 16))
        >> *.bild.de/* is available starting at age 12.

        This uses the API of https://www.jugendschutzprogramm.de/.
        :param url: the url to check (e.g. "bild.de" or "https://www.bild.de/")
        :param age: the age to check (e.g. 0, 6, 12, 16, 18)
        :return: a APIResult object containing the result of the check (see APIResult class)
        """

        hostname = urlparse(url).hostname
        if hostname is None:
            hostname = url

        result = requests.get(
            self.base_url,
            params={
                "url": hostname,
                "age": str(age),
                "otf": "y",
                "unk": "y",
                "par": "jpad",
                "tok": self.__generate_api_token(hostname),
            },
        )
        try:
            result = result.json()
        except requests.exceptions.JSONDecodeError:
            raise JugendschutzAPIClientException("The API returned an invalid result.")

        # replace hyphens with underscores
        result = {k.replace("-", "_"): v for k, v in result.items()}
        result["show"] = True if result["show"] == "1" else False
        result["cache"] = True if result["cache"] == "1" else False

        result["age"] = int(result["age"])

        result = APIResult(**result)
        return result


if __name__ == "__main__":
    client = JugendschutzAPIClient()
    print(client.check_url("bild.de", 16))
    print(client.check_url("https://bild.de", 16))
