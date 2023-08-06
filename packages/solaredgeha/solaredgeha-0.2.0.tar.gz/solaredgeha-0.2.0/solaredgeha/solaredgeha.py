import requests
from xml.etree import ElementTree


LOGINURL = 'https://api.solaredge.com/solaredge-apigw/api'
BASEURL = 'https://ha.monitoring.solaredge.com/api/homeautomation/v1.0'

COOKIE_NAME = "SPRING_SECURITY_REMEMBER_ME_COOKIE"


class SolaredgeHa(object):
    """
    Object containing SolarEdge's Home Automation site API-methods.
    """

    def __init__(self, username, password):
        """
        To communicate, you need to set a site and site token.
        Get it from your account.

        Parameters
        ----------
        username : str
        password : str
        """
        self.username = username
        self.password = password

        self.sites = []
        self.token = None

    def login(self):
        """
        Login to service

        Returns
        -------
        bool
        """

        url = urljoin(LOGINURL, "login")

        params = {
            "j_username": self.username,
            "j_password": self.password
        }

        r = requests.post(url, data=params, allow_redirects=False)

        r.raise_for_status()

        if (r.status_code != 302):
            return False

        self.token = r.cookies.get(COOKIE_NAME)

        return self.updateSites()

    def updateSites(self):
        """
        Update available sites

        Returns
        -------
        bool
        """

        if (self.token == None):
            return False

        url = urljoin(LOGINURL, "fields", "list")

        cookies = {
            COOKIE_NAME: self.token
        }

        r = requests.get(url, cookies=cookies)

        r.raise_for_status()

        tree = ElementTree.fromstring(r.content)

        self.sites = []
        for id in tree.iter('id'):
            self.sites.append(id.text)

        return True

    def ensureSession(self):
        if (self.token == None):
            self.login()

        return self.token != None

    def get_sites(self):
        """
        Get list of site ids

        Returns
        -------
        list
        """

        return self.sites

    def get_devices(self, site):
        """
        Request devices

        Returns
        -------
        dict
        """

        if (self.ensureSession() == False):
            return None

        url = urljoin(BASEURL, "sites", site, "devices")

        cookies = {
            COOKIE_NAME: self.token
        }

        r = requests.get(url, cookies=cookies)
        r.raise_for_status()
        return r.json()

    def activate_device(self, reporterId, level, duration=None):
        """
        Activate devices

        Returns
        -------
        dict
        """

        if (self.ensureSession() == False):
            return None

        url = urljoin(BASEURL, self.sites[0], "devices", reporterId, "activationState")

        cookies = {
            COOKIE_NAME: self.token
        }

        params = {
            "mode": "MANUAL",
            "level": level,
            "duration": duration
        }

        r = requests.put(url, json=params, cookies=cookies)
        r.raise_for_status()
        return r.json()


def urljoin(*parts):
    """
    Join terms together with forward slashes

    Parameters
    ----------
    parts

    Returns
    -------
    str
    """
    # first strip extra forward slashes (except http:// and the likes) and
    # create list
    part_list = []
    for part in parts:
        p = str(part)
        if p.endswith('//'):
            p = p[0:-1]
        else:
            p = p.strip('/')
        part_list.append(p)
    # join everything together
    url = '/'.join(part_list)
    return url
