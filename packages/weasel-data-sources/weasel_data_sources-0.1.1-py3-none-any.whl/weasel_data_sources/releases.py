""" Fetches release information and files from different data sources. """

import base64
import re

import requests


class ReleaseFetcher:
    """
    Base class of all release info fetchers.
    """

    def get_release_metadata(self) -> list:
        """
        Return a list of all releases known by the datasource

        :return:
        """
        raise NotImplementedError

    def get_file_list(self, version_str) -> dict:
        """
        Return a dict of files, including their size and optionally hashes for identification

        :param version_str: The version string of the release, i.e. '3.5.1'.
        :return:
        """
        raise NotImplementedError

    def retrieve_file(self, version_str, filename, target_path):
        """
        Stores a specified file in the given target location.

        :param version_str: The version string of the release, i.e. '3.5.1'.
        :param filename: The filename and path within the data source, i.e. 'foo/bar.txt'
        :param target_path: The path to which the retrieved file should be copied
        :return:
        """
        raise NotImplementedError


class CDNJSFetcher(ReleaseFetcher):
    """
    Fetcher to retrieve data from cdnjs.com
    """

    _re_sri = re.compile(r"(?P<algorithm>[^-]+)-(?P<b64hash>[\w+/]+==)")

    def __init__(self, library_name):
        self._library_name = library_name

        resp = requests.get("https://api.cdnjs.com/libraries/{}".format(library_name))
        resp.raise_for_status()
        data = resp.json()

        self._latest = data["version"]
        self._releases = {}
        for asset in data["assets"]:
            self._releases[asset["version"]] = {
                f: self._decode_hash(h) for f, h in asset["sri"].items()
            }

    def _decode_hash(self, sri):
        match = self._re_sri.fullmatch(sri)
        if match.group("algorithm") != "sha512":
            raise ValueError("Unsupported algorithm: " + match.group("algorithm"))

        return base64.standard_b64decode(match.group("b64hash")).hex()

    def get_release_metadata(self):
        return [
            {"version_str": ver, "latest": self._latest == ver}
            for ver in self._releases
        ]

    def get_file_list(self, version_str):
        return {
            file_name: {"hashes": {"sha512": hash_sum}}
            for file_name, hash_sum in self._releases[version_str].items()
        }

    def retrieve_file(self, version_str, filename, target_path):
        resp = requests.get(
            "https://cdnjs.cloudflare.com/ajax/libs/{}/{}/{}".format(
                self._library_name, version_str, filename
            ),
        )
        resp.raise_for_status()

        with open(target_path, "wb") as file:
            file.write(resp.content)
