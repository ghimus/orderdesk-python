from urllib.parse import urljoin

import json
import os
import requests


class OrderDeskBaseClient(object):
    def __init__(self, store_id=None, apikey=None):
        self.endpoint = 'https://app.orderdesk.me/api/v2/'
        self.store_id = os.environ.get('ORDERDESK_STORE_ID', store_id)
        self.apikey = os.environ.get('ORDERDESK_APIKEY', apikey)

        if not self.store_id:
            raise ValueError(
                'Please specify ORDERDESK_STORE_ID in your environment '
                'or through the client as `store_id`')

        if not self.apikey:
            raise ValueError(
                'Please specify ORDERDESK_APIKEY in your environment '
                'or through the client as `apikey`')

        self.headers = {
            'ORDERDESK-STORE-ID': self.store_id,
            'ORDERDESK-API-KEY': self.apikey,
            'Content-Type': 'application/json',
        }

    def send_response(self, response):
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {
                'status': 'error',
                'message': 'HTTP %s' % response.status_code,
            }

    def get(self, method, data={}):
        return self.send_response(
            requests.get(
                urljoin(self.endpoint, method),
                params=data,
                headers=self.headers))

    def post(self, method, data={}):
        return self.send_response(
            requests.post(
                urljoin(self.endpoint, method),
                data=json.dumps(data),
                headers=self.headers))

    def put(self, method, data={}):
        return self.send_response(
            requests.put(
                urljoin(self.endpoint, method),
                data=json.dumps(data),
                headers=self.headers))

    def delete(self, method={}):
        return self.send_response(
            requests.delete(
                urljoin(self.endpoint, method),
                headers=self.headers))
