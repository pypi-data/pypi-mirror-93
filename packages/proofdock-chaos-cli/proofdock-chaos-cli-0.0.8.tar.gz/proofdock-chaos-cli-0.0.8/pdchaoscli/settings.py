import os
from typing import Dict
from chaoslib.types import Control, Settings

DEFAULT_PROOFDOCK_API_URL = 'https://chaosapi.proofdock.io/'
PDCLI_CONFIG_PATH = os.path.abspath(os.path.expanduser("~/.pdcli/settings.yaml"))


def get_api_url(settings: Settings) -> str:
    """Get the Proofdock API endpoint.
    """
    return _get_endpoint(settings).get('url', '')


def get_api_token(settings: Settings) \
        -> str:
    """Get the token for the Proofdock API endpoint.
    """
    return _get_endpoint(settings).get('token', '')


def get_attack(settings: Settings):
    """Return current attack
    """
    return _get_proofdock(settings)['attack']


def set_attack(settings: Settings, attack: Dict):
    _get_proofdock(settings)['attack'] = attack


def set_endpoint(settings: Settings, endpoint: Dict):
    if not endpoint.get('url'):
        endpoint['url'] = DEFAULT_PROOFDOCK_API_URL
    _get_proofdock(settings)['endpoint'] = endpoint


def _get_proofdock(settings: Settings) -> Control:
    return settings.setdefault('proofdock', {})


def _get_endpoint(settings: Settings) -> Control:
    return _get_proofdock(settings).setdefault('endpoint', {})
