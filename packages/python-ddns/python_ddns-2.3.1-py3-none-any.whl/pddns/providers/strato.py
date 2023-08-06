"""Module for using Strato's API"""
import logging
import requests


class Strato:  # pylint: disable=too-few-public-methods
    """Strato
    ---

    Class that deals with records for Strato.
    """

    def __init__(self, CONFIG, version):
        self.Config = CONFIG["Strato"]
        self.log = logging.getLogger("PDDNS")
        self.version = version

        self.log.info("Strato selected")

    def main(self, ip: str, ipv6: str) -> None:
        """main
        ---

        Arguments:
        ---
            ip {str} -- The IP address that the new record will have.
        """
        new_ips = ip + "," + ipv6
        new_ips = new_ips.strip(",")
        login_data = f"{self.Config['User']}:{self.Config['Password']}"
        BASE_URL = f"https://{login_data}@dyndns.strato.com/nic/update"
        header = {"User-Agent": "PDDNS v{}".format(self.version)}
        data = {"hostname": self.Config["Name"], "myip": new_ips}
        r = requests.get(BASE_URL, params=data, headers=header)
        self.log.debug(r.text)
        r.raise_for_status()
