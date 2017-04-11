import logging
import requests
import config


class ApiClient:

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.host = config.API_HOST

    @staticmethod
    def get_answer_body(data):
        """
        Returns answer body
        :param data: 
        :return: 
        """
        return data.json()\
            if data.text.strip() and 'json' in data.headers.get('Content-Type')\
            else data.text

    @staticmethod
    def is_success_request(data):
        """
        Returns success flag
        :param data: 
        :return: 
        """
        return 200 <= data.status_code < 300

    def make_request(self, method, resource, host=None, headers=None, json=None):
        """
        Makes request
        :param str method: 
        :param str resource: 
        :param str host: 
        :param dict headers: 
        :param dict json: 
        :return: 
        """
        if not host:
            host = self.host

        self.log.debug('{} request: {}{} {}'.format(
            method, host, resource, json
        ))

        data = requests.request(
            method, host + resource, headers=headers, json=json
        )

        self.log.debug('Response: {}. Status code: {}'.format(
            data.text, data.status_code
        ))

        return {
            'data': self.get_answer_body(data),
            'success': self.is_success_request(data),
            'status_code': data.status_code
        }
