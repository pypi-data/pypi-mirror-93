"""
Easy to use urllib3 simplifier.


Usage:
```
>>> client = simpleurllib3.Client()
>>> resp = client.get('http://httpbin.org/ip')
>>> resp.status
200
>>> resp.data
"{'origin': '127.0.0.1'}"
"""
import warnings
import pkg_resources
import urllib3
import certifi
import luddite


class OutdatedModuleWarning(ImportWarning):
    """
    ImportWarning class for outdated modules.
    """


def _outdated_warn(module_name: str, *extra_msg):
    """
    Execute warnings.warn for OutdatedModuleWarning.
    """
    message = f'Module "{module_name}" outdated'
    if extra_msg:
        warnings.warn(f"{message}, {extra_msg[0]}",  OutdatedModuleWarning)
    else:
        warnings.warn(message, OutdatedModuleWarning)


def _get_package_version(package_name: str):
    """
    Get the installed package's version.
    """
    return pkg_resources.get_distribution(package_name).version


warnings.simplefilter("module", category=OutdatedModuleWarning)
if luddite.get_version_pypi('urllib3') != _get_package_version('urllib3'):
    _outdated_warn("urllib3")


class SSLClient:
    """
    Secure SSL PoolManager client.
    """
    if luddite.get_version_pypi('certifi') != _get_package_version('certifi'):
        _outdated_warn("certifi", "SSL might not work properly")
    ssl_poolmanager = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )

    def get(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.ssl_poolmanager.request_encode_url("GET", url, fields=fields, headers=headers)

    def post(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.ssl_poolmanager.request_encode_body("POST", url, fields=fields, headers=headers)

    def put(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.ssl_poolmanager.request_encode_body("PUT", url, fields=fields, headers=headers)

    def delete(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.ssl_poolmanager.request_encode_url("DELETE", url, fields=fields, headers=headers)

    def patch(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.ssl_poolmanager.request_encode_body("PATCH", url, fields=fields, headers=headers)

    def head(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.ssl_poolmanager.request_encode_url("HEAD", url, fields=fields, headers=headers)

    def options(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.ssl_poolmanager.request_encode_url("OPTIONS", url, fields=fields, headers=headers)


class Client:
    """
    PoolManager client.
    """
    poolmanager = urllib3.PoolManager()

    def get(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.poolmanager.request_encode_url("GET", url, fields=fields, headers=headers)

    def post(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.poolmanager.request_encode_body("POST", url, fields=fields, headers=headers)

    def put(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.poolmanager.request_encode_body("PUT", url, fields=fields, headers=headers)

    def delete(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.poolmanager.request_encode_url("DELETE", url, fields=fields, headers=headers)

    def patch(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.poolmanager.request_encode_body("PATCH", url, fields=fields, headers=headers)

    def head(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.poolmanager.request_encode_url("HEAD", url, fields=fields, headers=headers)

    def options(self, url, fields=None, headers=None):
        """
        Returns urllib3.response.HTTPResponse,
        refer to urllib3 docs for more info.
        """
        return self.poolmanager.request_encode_url("OPTIONS", url, fields=fields, headers=headers)
