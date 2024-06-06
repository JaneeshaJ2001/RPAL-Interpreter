from ASTNode import ASTNode
import logging

class Environment:
    logger = logging.getLogger(__name__)

    def __init__(self, index):
        self.idx = index
        self.map_vars = {}
        self.parent = None

    def set_env_params(self, parent_env, key, value):
        self.map_vars[key] = value
        if isinstance(key, ASTNode) and isinstance(value, ASTNode):
            pass
        else:
            pass
        self.parent = parent_env

    def get_env_idx(self):
        return self.idx

    def get_val(self, key):
        if key in self.map_vars.keys():
            value = self.map_vars[key]
            self.logger.info("found in cur env id {}".format(self.idx))
            if isinstance(value, ASTNode):
                self.logger.info("value: {}".format(value.value))
            return value
        else:
            self.logger.info("not found in cur env")
            return None
