from jeri.core.backends.backend import Backend
import re
import requests


def _get(url, params=None):
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise RuntimeError('API call failed')
    return response.json()


def _get_all(url, offset=0):
    parameters = {'offset': offset}
    response = _get(url, parameters)
    return (response['objects'], response['meta']['total_count'])


class TastypieBackend(Backend):

    def __init__(self, base_url):
        if base_url is None or base_url == "":
            raise RuntimeError('TastypieBackend cannot have an empty base_url')
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'

    def get(self, model, **kwargs):
        if 'uri' in kwargs:
            object = _get(self._uri_to_url(model, kwargs['uri']))
        return object

    def get_all(self, model, **kwargs):
        objects, count = _get_all(self._url(model))
        offset = len(objects)
        while offset != count:
            objects.extend(_get_all(self._url(model), offset)[0])
            offset = len(objects)
        return objects

    @property
    def id_key(self):
        return 'id'

    @property
    def uri_key(self):
        return 'resource_uri'

    def _url(self, model):
        return self.base_url + model._meta.endpoint + '/'

    def _uri_to_url(self, model, uri):
        expr = r'.*/{}/(?P<id>[0-9]*)/?'.format(model._meta.endpoint)
        match = re.match(expr, uri)
        return self._url(model) + match['id'] + '/'
