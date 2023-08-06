#coding:utf-8
import json
from typing import List
import chardet
import requests
import urllib.parse
from requests.utils import guess_json_utf

from winney.mock import Mock
from winney.errors import NoServerAvalible, WinneyParamError


class Result(object):
    def __init__(self, resp=None, url=None, method=None):
        if resp and not isinstance(resp, requests.Response):
            raise WinneyParamError(
                "resp should be object of requests.Response, but {} found.".
                format(type(resp)))
        self.status = resp.ok if resp else False
        self.reason = resp.reason if resp else None
        self.content = resp.content if resp else None
        self.headers = resp.headers.__repr__() if resp else None
        self.encoding = resp.encoding if resp else None
        self.status_code = resp.status_code if resp else None
        self.request_url = url
        self.request_method = method
        # self.encoding = None

    def ok(self):
        return self.status

    def get_bytes(self):
        return self.content

    def get_text(self):
        """
        Quoted from: requests.models.text()
        """
        text = None
        if not self.encoding:
            self.encoding = chardet.detect(self.content)["encoding"]
        try:
            text = str(self.content, self.encoding, errors='replace')
        except (LookupError, TypeError):
            text = str(self.content, errors='replace')
        return text

    def get_json(self, **kwargs):
        """
        Quoted from: requests.models.json()
        """
        if not self.encoding:
            self.encoding = chardet.detect(self.content)["encoding"]
        if not self.encoding and self.content and len(self.content) > 3:
            # No encoding set. JSON RFC 4627 section 3 states we should expect
            # UTF-8, -16 or -32. Detect which one to use; If the detection or
            # decoding fails, fall back to `self.text` (using chardet to make
            # a best guess).
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return json.loads(self.content.decode(encoding), **kwargs)
                except UnicodeDecodeError:
                    pass
        return json.loads(self.get_text(), **kwargs)

    def json(self, **kwargs):
        return self.get_json(**kwargs)


class Address(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port


def retry(func):
    def wrapper(self, *args, **kwargs):
        counter = 0
        while counter < len(self.winney.addrs):
            try:
                counter += 1
                r = func(self, *args, **kwargs)
            except Exception as e:
                print(e)
                self.winney._next()
                continue
            return r
        raise NoServerAvalible(
            "cannot find an avalible server for request: {}".format(
                self.winney.url))

    return wrapper


class Winney(object):
    def __init__(self,
                 host,
                 port=80,
                 protocol="http",
                 addrs: List[Address] = None,
                 headers=None,
                 base_path=""):
        self.host = host
        self.port = port
        self.headers = headers
        self.protocol = protocol
        self.base_path = base_path
        self.addrs = addrs if addrs else []
        self._index = 0
        self.domain = ""
        self.url = ""
        self.result = {}
        self.apis = []
        self.build_domain()

    def _next(self):
        if not self.addrs:
            return
        self._index = (self._index + 1) % len(self.addrs)
        self.host = self.addrs[self._index].host
        self.port = self.addrs[self._index].port
        self.build_domain()

    def build_domain(self):
        self.domain = "{}://{}:{}".format(self.protocol, self.host, self.port)

    def _bind_func_url(self, url, method, mock=False, mock_data=None):
        def req(data=None, json=None, files=None, headers=None, **kwargs):
            url2 = url.format(**kwargs)
            if mock:
                r = Result(url=url2, method=method)
                r.status = True
                r.encoding = "utf8"
                r.content = bytes(mock_data.to_string(), encoding=r.encoding)
                return r
            r = self.request(method, url2, data, json, files, headers)
            # if r.status_code > 200, not r is True
            # if not r:
            #     raise WinneyRequestError(
            #         "failed to request url = {}, it returned null".format(
            #             url2))
            return Result(r, url2, method)

        return req

    def register(self, method, name, uri, mock=False, mock_data: Mock = None):
        if mock and not isinstance(mock_data, Mock):
            raise WinneyParamError(
                "mock_data should be type of winney.Mock, but type {} found".
                format(type(mock_data)))
        method = method.upper()
        name = name.lower()
        if name in self.apis:
            raise WinneyParamError("Duplicate name = {}".format(name))
        setattr(self, name, self._bind_func_url(uri, method, mock, mock_data))
        self.apis.append(name)
        return getattr(self, name)

    def request(self,
                method,
                url,
                data=None,
                json=None,
                files=None,
                headers=None):
        # 每次请求都计算 url，因为有遇到 url 改变的情况
        url = "/".join([self.base_path, url]).replace("//", "/").replace("//", "/") \
                if self.base_path else url
        self.url = url
        url = urllib.parse.urljoin(self.domain, url)
        if headers and isinstance(headers, dict):
            if self.headers:
                for key, value in self.headers.items():
                    if key in headers:
                        continue
                    headers[key] = value
        else:
            headers = self.headers
        if method.upper() == "GET":
            return self.get(url, data, headers=headers)
        if method.upper() == "POST":
            return self.post(url,
                             data=data,
                             json=json,
                             files=files,
                             headers=headers)
        if method.upper() == "PUT":
            return self.put(url,
                            data=data,
                            json=json,
                            files=files,
                            headers=headers)
        if method.upper() == "DELETE":
            return self.delete(url, data=data, headers=headers)

    def get(self, url, data=None, headers=None):
        return requests.get(url, params=data, headers=headers)

    def post(self, url, data=None, json=None, files=None, headers=None):
        return requests.post(url,
                             data=data,
                             json=json,
                             files=files,
                             headers=headers)

    def put(self, url, data=None, json=None, files=None, headers=None):
        return requests.put(url, data, json=json, files=files, headers=headers)

    def delete(self, url, data=None, headers=None):
        return requests.delete(url, data=data, headers=headers)

    def options(self, url, headers=None):
        return requests.options(url, headers=headers)
