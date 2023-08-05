import os

from logzero import logger

import pdchaoscli.api.attacks as attacks
import pdchaoscli.api.scenarios as scenarios
from pdchaoscli.api.session import client_session


def load_attack(settings, definition_id):
    """Load the attack safely."""
    attack = _get_attack_from_endpint(settings, definition_id)
    # fallback - check if this is scenario
    if not attack:
        scenario = _get_scenario_from_endpoint(settings, definition_id)
        pipeline_info = load_pipeline_info()
        with client_session(verify_tls=False, settings=settings) as session:
            attack = scenarios.create_attack(scenario['id'], pipeline_info, session)
    if not attack:
        raise Exception('Unable to load attack.')

    if str(attack.get('status')).lower() != 'pending':
        raise Exception('Invalid attack id, attack was already executed.')

    return attack


def _get_attack_from_endpint(settings, definition_id):
    attack = None
    with client_session(verify_tls=False, settings=settings) as session:
        try:
            attack = attacks.get_attack(definition_id, session)
        except Exception:
            logger.debug('No attack definition found.', exc_info=1)
    return attack


def _get_scenario_from_endpoint(settings, scenario_id):
    """Load the attack or scenario safely."""
    scenario = None
    with client_session(verify_tls=False, settings=settings) as session:
        try:
            scenario = scenarios.get_scenario(scenario_id, session)
        except Exception:
            logger.debug('No scenario definition found.', exc_info=1)
    return scenario


def load_endpoint():
    return {
        'url': _get_variable_or_default('PROOFDOCK_API_URL', None),
        'token': _get_variable_or_default('PROOFDOCK_API_TOKEN', None)
    }


def load_pipeline_info():
    return {
        'pipeline_id': _get_variable_or_default('PROOFDOCK_PIPELINE_ID', None),
        'pipeline_run_id': _get_variable_or_default('PROOFDOCK_PIPELINE_RUN_ID', None),
        'pipeline_run_name': _get_variable_or_default('PROOFDOCK_PIPELINE_RUN_NAME', None),
        'pipeline_run_url': _get_variable_or_default('PROOFDOCK_PIPELINE_RUN_URL', None)
    }


def _get_variable_or_default(var: str, default: str):
    if var in os.environ and os.environ[var]:
        return os.environ[var]
    else:
        return default
