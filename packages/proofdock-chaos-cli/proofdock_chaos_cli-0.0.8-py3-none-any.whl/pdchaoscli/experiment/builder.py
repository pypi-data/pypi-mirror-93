from __future__ import annotations

from typing import Dict

from chaoslib.types import Experiment
from pdchaoscli.experiment.activity import AttackActivity


def build(attack: Dict) -> Experiment:
    definition = attack.get('definition')
    title = definition.get('title') or 'Attack'
    description = definition.get('description') or 'Attack'

    experiment = _get_experiment_template()
    if len(definition.get('method')) > 0:
        # set meta data of experiment
        _set_experiment_meta(experiment, title, description)
        # set method section
        for item in definition.get('method'):
            attack_activity = AttackActivity.get(item)
            attack_activity.add_to_experiment(experiment)

    return experiment


def _get_experiment_template():
    return {
        "version": "1.0.0",
        "title": "",
        "description": "",
        "method": [],
        "rollbacks": []
    }


def _set_experiment_meta(experiment: Experiment, title: str, description: str):
    experiment['title'] = title
    experiment['description'] = description
