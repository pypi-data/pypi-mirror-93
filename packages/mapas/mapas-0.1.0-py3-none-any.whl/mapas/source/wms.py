from typing import Tuple, Dict, List

from .base import ImageSource


class ImageWms(ImageSource):
    def __init__(
            self, server_url: str, layers: List[str], *, cql_filter: str = ''):
        self.server_url = server_url
        self.layers = layers
        self.cql_filter = cql_filter

    def get_uri_for_resource(
            self, bbox: Tuple[float, float, float, float],
            dimensions: Tuple[int, int]) -> str:
        return self.server_url

    def get_request_params(
            self, bbox: Tuple[float, float, float, float],
            dimensions: Tuple[int, int]) -> Dict[str, str]:
        return {
            'SERVICE': 'WMS',
            'VERSION': '1.1.1',
            'REQUEST': 'GetMap',
            'FORMAT': 'image/png',
            'TRANSPARENT': 'true',
            'LAYERS': ','.join(self.layers),
            'exceptions': 'application/vnd.ogc.se_inimage',
            'CQL_FILTER': self.cql_filter,
            'SRS': 'EPSG:3857',
            'STYLES': '',
            'WIDTH': dimensions[0],
            'HEIGHT': dimensions[1],
            'BBOX': ','.join(map(str, bbox)),
        }
