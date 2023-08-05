from skyext.base_class.action_base import BaseAction
from model1 import validator_schema_dict


class Model1BaseAction(BaseAction):
    def _get_app_validator_schemas(self, cls_name, fun_name, **params):
        return validator_schema_dict
