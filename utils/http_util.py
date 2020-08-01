import json

import requests


class HttpUtil:
    def post(url, data, headers, convert_data_to_json_str=True):
        if convert_data_to_json_str:
            res = requests.post(url=url, headers=headers, data=json.dumps(data))
        else:
            res = requests.post(url=url, headers=headers, data=data)
        if res.status_code <= 400:
            return res.content
        raise Exception(res.content)

    def get(url, headers):
        res = requests.get(url=url, headers=headers)
        if res.status_code <= 400:
            return res.content
        raise Exception(res.content)
