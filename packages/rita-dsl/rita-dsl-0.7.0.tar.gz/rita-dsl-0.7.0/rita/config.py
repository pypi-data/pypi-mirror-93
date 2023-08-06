import operator
import logging
from importlib import import_module

try:
    from rita.engine.translate_spacy import compile_rules as spacy_engine
except ImportError:
    pass

from rita.engine.translate_standalone import compile_rules as standalone_engine
from rita.engine.translate_rust import compile_rules as rust_engine

from rita.utils import SingletonMixin


logger = logging.getLogger(__name__)


class Config(SingletonMixin):
    def __init__(self):
        self.available_engines = []
        self.engines_by_key = {}
        self.current_engine = None

        try:
            self.register_engine(1, "spacy", spacy_engine)
        except NameError:
            # spacy_engine is not imported
            pass
        self.register_engine(2, "standalone", standalone_engine)
        self.register_engine(3, "rust", rust_engine)

    def register_engine(self, priority, key, compile_fn):
        self.available_engines.append((priority, key, compile_fn))
        self.engines_by_key[key] = compile_fn
        sorted(self.available_engines, key=operator.itemgetter(0))

    @property
    def default_engine(self):
        (_, key, compile_fn) = self.available_engines[0]
        self.current_engine = key
        return compile_fn

    def set_engine(self, key):
        self.current_engine = key
        return self.engines_by_key[key]

    @property
    def list_branching(self):
        if self.current_engine == "spacy":
            return True

        return False


class SessionConfig(object):
    def __init__(self):
        self._root = Config()
        self.modules = []
        # Default config
        self._data = {
            "ignore_case": True,
            "implicit_punct": True,
            "deaccent": True,
            "implicit_hyphon": False,
        }
        self.variables = {}
        self._nested_group_count = 0

    def register_module(self, mod_name):
        logger.debug("Importing module: {}".format(mod_name))
        self.modules.append(import_module(mod_name))

    def set_variable(self, k, v):
        self.variables[k] = v

    def get_variable(self, k):
        return self.variables[k]

    def __getattr__(self, name):
        if name == "_root":
            return self._root

        elif name in self._data:
            return self._data[name]

        return getattr(self._root, name)

    def set_config(self, k, v):
        # Handle booleans first
        if v.upper() in ["1", "T", "Y"]:
            self._data[k] = True
        elif v.upper() in ["0", "F", "N"]:
            self._data[k] = False
        else:
            self._data[k] = v

    def new_nested_group_id(self):
        self._nested_group_count += 1
        return self._nested_group_count


def with_config(fn):
    def wrapper(*args, **kwargs):
        config = SessionConfig()
        return fn(*args, config=config, **kwargs)

    return wrapper
