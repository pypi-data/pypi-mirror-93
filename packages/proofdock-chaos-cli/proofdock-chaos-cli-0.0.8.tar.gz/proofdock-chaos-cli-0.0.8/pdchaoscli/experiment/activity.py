from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict, List

from chaoslib.types import Experiment


class AttackActivity(object):
    # application domain related constants
    DOMAIN_APPLICATION = 'application'

    # azure domain related constants
    DOMAIN_AZURE = 'azure'
    DOMAIN_AZURE_WEB_APP = 'webapp'
    DOMAIN_AZURE_VIRTUAL_MACHINE = 'vm'
    DOMAIN_AZURE_AVAILABILITY_SET = 'vmas'
    DOMAIN_AZURE_SCALE_SET = 'vmss'

    # common domain
    DOMAIN_COMMON = 'common'
    DOMAIN_COMMON_DELAY = 'delay'

    def __init__(self, activity: Dict[str, Any]):
        self._activity = activity

    @staticmethod
    def get(activity: Dict[str, Any]):
        activity_type: str = activity.get('type')
        activity_type_split = activity_type.split(".")
        domain_provided = activity_type_split[0]

        if len(activity_type_split) == 1:
            # Invalid activity value
            raise Exception("Unsupported activity type")
        elif domain_provided.lower() == AttackActivity.DOMAIN_APPLICATION:
            return ApplicationAttackActivity(activity)
        elif domain_provided.lower() == AttackActivity.DOMAIN_AZURE:
            resource_type = activity_type_split[1]
            if AttackActivity.DOMAIN_AZURE_WEB_APP in resource_type:
                return AzureAttackWebAppActivity(activity)
            elif AttackActivity.DOMAIN_AZURE_AVAILABILITY_SET in resource_type:
                return AzureAttackVirtualMachineActivity(activity)
            elif AttackActivity.DOMAIN_AZURE_SCALE_SET in resource_type:
                return AzureAttackScaleSetActivity(activity)
            elif AttackActivity.DOMAIN_AZURE_VIRTUAL_MACHINE in resource_type:
                return AzureAttackVirtualMachineActivity(activity)
            else:
                raise Exception("Unsupported azure resource_type type")
        elif domain_provided.lower() == AttackActivity.DOMAIN_COMMON:
            func = activity_type_split[1]
            if func == AttackActivity.DOMAIN_COMMON_DELAY:
                return DelayActivity(activity)
            else:
                raise Exception("Unsupported function")
        else:
            # Nothing matches
            raise Exception("Unsupported activity type")

    @property
    def type(self) -> str:
        return self._activity.get('type')

    @abstractmethod
    def add_to_experiment(self, experiment: Experiment):
        raise NotImplementedError()

    @property
    def arguments(self) -> str:
        return self._activity.get('arguments')


class ApplicationAttackActivity(AttackActivity):
    def __init__(self, activity: Dict[str, Any]):
        AttackActivity.__init__(self, activity)
        activity_type_split = self.type.split(".")
        if activity_type_split[1].lower() != 'attack_request':
            raise Exception("Unsupported application activity type")

    def add_to_experiment(self, experiment: Dict[str, Any]):
        # start attack and pause for a request attack duration
        method = experiment.get('method')
        method.append({
            "type": "action",
            "name": "Inject application attack",
            "provider": {
                "type": "python",
                "module": "pdchaoscli.application.actions",
                "func": "start_attack",
                "arguments": {
                    "actions": self.arguments.get('actions'),
                    "path": self.arguments.get('path'),
                    "targets": self.arguments.get('targets')
                }
            },
            "pauses": {
                "after": self.arguments.get('duration')
            }
        })
        rollbacks = experiment.get('rollbacks')
        rollbacks.append({
            "type": "action",
            "name": "Cancel application attack",
            "provider": {
                "type": "python",
                "module": "pdchaoscli.application.actions",
                "func": "cancel_attack",
                "arguments": {
                    "targets": self.arguments.get("targets")
                }
            }
        })


class AzureAttackActivity(AttackActivity):
    def __init__(self, activity: Dict[str, Any]):
        AttackActivity.__init__(self, activity)

    def get_function(self) -> str:
        activity_type_split = self._activity.get('type').split(".")
        return activity_type_split[2]

    def get_filter(self):
        if len(self._activity.get('arguments').get('resources')) == 0:
            return ""
        where = None
        for resource in self._activity.get('arguments').get('resources'):
            if not where:
                where = f"where id=~'{resource.get('id')}'"
            else:
                where = where + f" or id=~'{resource.get('id')}'"
        return where

    @abstractmethod
    def get_method_activities(self) -> List[Any]:
        raise NotImplementedError()

    def get_rollbacks(self) -> List[Any]:
        return []

    def add_to_experiment(self, experiment: Dict[str, Any]):
        # start attack and pause for a request attack duration
        method = experiment.get('method')
        method.extend(self.get_method_activities())
        rollbacks = experiment.get('rollbacks')
        rollbacks.extend(self.get_rollbacks())


class AzureAttackWebAppActivity(AzureAttackActivity):
    def get_method_activities(self):
        return [{
            "type": "action",
            "name": f"Inject web app attack {self.get_function()}",
            "provider": {
                "type": "python",
                "module": "pdchaosazure.webapp.actions",
                "func": self.get_function(),
                "arguments": {
                    "filter": self.get_filter()
                }
            }
        }]


class AzureAttackVirtualMachineActivity(AzureAttackActivity):
    def get_method_activities(self) -> List[Any]:
        return [{
            "type": "action",
            "name": f"Inject virtual machine attack: {self.get_function()}",
            "provider": {
                "type": "python",
                "module": "pdchaosazure.vm.actions",
                "func": self.get_function(),
                "arguments": {
                    "filter": self.get_filter()
                }
            }
        }]


class AzureAttackScaleSetActivity(AzureAttackActivity):
    def get_vmss_filter(self):
        if len(self._activity.get('arguments').get('resources')) == 0:
            return ""
        where = None
        vmss_set = self.collect_scale_sets()
        for set in vmss_set:
            if not where:
                where = f"where id=~'{set}'"
            else:
                where = where + f" or id=~'{set}'"
        return where

    def get_instances_filter(self):
        if len(self._activity.get('arguments').get('resources')) == 0:
            return ""
        where = None
        for instance in self._activity.get('arguments').get('resources'):
            index = instance.get('id').rindex('/') + 1
            instance_id = instance.get('id')[index:]
            if not where:
                where = f"where instance_id=='{instance_id}'"
            else:
                where = where + f" or instance_id=='{instance_id}'"
        return where

    def collect_scale_sets(self):
        vmss_set = set()
        for instance in self._activity.get('arguments').get('resources'):
            index = instance.get('id').index("/virtualMachines/")
            vmss_set.add(instance.get('id')[:index])
        return vmss_set

    def get_method_activities(self) -> List[Any]:
        return [{
            "type": "action",
            "name": f"Inject scale set attack: {self.get_function()}",
            "provider": {
                "type": "python",
                "module": "pdchaosazure.vmss.actions",
                "func": self.get_function(),
                "arguments": {
                    "vmss_filter": self.get_vmss_filter(),
                    "instance_filter": self.get_instances_filter()
                }
            }
        }]


class DelayActivity(AttackActivity):
    def __init__(self, activity: Dict[str, Any]):
        AttackActivity.__init__(self, activity)

    def add_to_experiment(self, experiment: Dict[str, Any]):
        # start attack and pause for a request attack duration
        method = experiment.get('method')
        if len(method) < 1:
            return
        activity = method[-1]
        delay = int(self.arguments.get('duration'))
        if "pauses" in activity:
            delay = int(activity.get('pauses').get('after')) + delay
        activity.update({
            "pauses": {
                "after": delay
            }
        })
