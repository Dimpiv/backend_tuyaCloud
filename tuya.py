import requests
import hmac
import hashlib
import time
import configparser
import sys


class TuyaMessages:

    def __init__(self):
        config = configparser.ConfigParser()

        try:
            config.read("config.ini")
            self.AccessId = config.get("tuya", "AccessId")
            self.AccessKey = config.get("tuya", "AccessKey")
            self.ServerUrl = config.get("tuya", "ServerUrl")
            self.Schema = config.get("tuya", "Schema")
        except configparser.NoSectionError:
            print("Error read config")
            sys.exit(0)

        self.errors = dict()
        self.tokens = dict()
        self.refresh_token = str()
        self.easy_token = str()
        self.expire_time = int()

    def ok(self, data: dict) -> bool:
        result = data.get("success", False)
        if result:
            self.tokens = data.get("result", dict())
            self.easy_token = self.tokens.get("access_token", "")
            self.refresh_token = self.tokens.get("refresh_token", "")
            self.expire_time = self.tokens.get("expire_time", 10)
        else:
            self.errors["msg"] = data.get("msg")
            self.errors["code"] = data.get("code")
            print(self.errors)
        return result


class Core(TuyaMessages):

    @staticmethod
    def get_timestamp() -> int:
        return int(round(time.time() * 1000))

    def headers(self) -> dict:
        t = self.get_timestamp()
        headers = {"client_id": self.AccessId,
                   "sign": self.gen_sign(t),
                   "sign_method": "HMAC-SHA256",
                   "t": str(t)}
        return headers

    def gen_sign(self, t: int, input_string="") -> str:
        secret_key = self.AccessKey.encode("utf-8")
        if input_string:
            total_params = input_string
        else:
            total_params = self.AccessId + str(t)
        signature = hmac.new(secret_key, total_params.encode("utf-8"), hashlib.sha256).hexdigest()
        result = "{0}".format(signature)
        return result.upper()

    def get_token(self) -> dict:
        url = "/v1.0/token?grant_type=1"
        r = requests.get(self.ServerUrl + url, headers=self.headers())
        return r.json()

    def update_token(self) -> dict:
        url = "/v1.0/token/" + self.refresh_token
        r = requests.get(self.ServerUrl + url, headers=self.headers())
        return r.json()

    def check_timeout_token(self):
        if self.expire_time < 100:
            if not self.ok(self.update_token()):
                self.ok(self.get_token())

    def check_token(self):
        if not self.easy_token:
            self.ok(self.get_token())
        else:
            self.check_timeout_token()
