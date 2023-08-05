import json
from datetime import datetime
from typing import Dict

from pdchaoscli.api import get_error_message
from pdchaoscli.api.endpoints import scenario, scenario_attacks, scenario_events
from requests import Session


def get_scenario(scenario_id: str, session: Session):
    response = session.get(scenario(scenario_id), timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))


def create_attack(scenario_id: str, pipeline_info: Dict, session: Session):
    data = json.dumps(pipeline_info)
    response = session.post(scenario_attacks(scenario_id),  data=data, timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))


def send_execution_event(execution_id: str, name: str, context: Dict, state, session: Session):
    data = json.dumps({
        'name': name,
        'state': state,
        'context': context,
        'timestamp': datetime.utcnow().isoformat()
    })
    response = session.post(scenario_events(execution_id), data=data, timeout=30)
    if not response.ok:
        raise Exception(get_error_message(response))
