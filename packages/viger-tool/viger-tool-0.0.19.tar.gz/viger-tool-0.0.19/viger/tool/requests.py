#!/usr/bin/env python

import io
import sys
import requests
from .json import json
from .result import Result

# Format Request
class Requests():
    """
    包裝request方法，
    只支援JSON格式，
    return Result
    """
    def __init__(self, *args, **kwargs):
        # 取消告警
        requests.packages.urllib3.disable_warnings()

        self.header = {
            'Content-Type': 'application/json',
        }
        self.timeout = kwargs.get('timeout', 10)
        self.result = Result()

    def get(self, url, body={}):
        """
        通用Get方法
        """
        try:
            resp = requests.get(url, json=body, headers=self.header,
                    timeout=self.timeout, verify=False)
            if resp.status_code != 200:
                self.result.set(resp.text, False)
                return self.result
            self.result.set(json.loads(resp.text))
        except json.decoder.JSONDecodeError:
            self.result.set(resp.text, False)
        except Exception as e:
            self.result.set(str(e), False)
        return self.result

    def post(self, url, body=None):
        """
        通用Post方法
        """
        try:
            resp = requests.post(url, json=body, headers=self.header,
                    timeout=self.timeout, verify=False)
            if resp.status_code not in [200, 201, 202, 204]:
                self.result.set(resp.text, False)
                return self.result
            self.result.set(json.loads(resp.text))
        except json.decoder.JSONDecodeError:
            self.result.set(resp.text, False)
        except Exception as e:
            self.result.set(str(e), False)
        return self.result

    def put(self, url, body=None):
        """
        通用Put方法
        """
        try:
            resp = requests.put(url, json=body, headers=self.header,
                    timeout=self.timeout, verify=False)
            if resp.status_code not in [200, 201, 202, 204]:
                self.result.set(resp.text, False)
                return self.result
            self.result.set(json.loads(resp.text))
        except json.decoder.JSONDecodeError:
            self.result.set(resp.text, False)
        except Exception as e:
            self.result.set(str(e), False)
        return self.result

    def delete(self, url, body=None):
        """
        通用Delete方法
        """
        try:
            resp = requests.delete(url, json=body, headers=self.header,
                    timeout=self.timeout, verify=False)
            if resp.status_code not in [200, 201, 202, 204]:
                self.result.set(resp.text, False)
                return self.result
            if resp.text:
                self.result.set(json.loads(resp.text))
            else:
                self.result.set('')
        except json.decoder.JSONDecodeError:
            self.result.set(resp.text, False)
        except Exception as e:
            self.result.set(str(e), False)
        return self.result