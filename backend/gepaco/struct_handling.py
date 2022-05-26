import importlib.util
import sys
import inspect
import hydration
from typing import Dict


def load_module(path: str):
    spec = importlib.util.spec_from_file_location("module.name", path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = foo
    spec.loader.exec_module(foo)
    return foo


def load_structs_from_path(path: str) -> Dict[str, type]:
    module = load_module(path)

    structs = {}
    for item_key in module.__dict__:
        item = getattr(module, item_key)
        if not inspect.isclass(item):
            continue
        
        if issubclass(item, hydration.Struct):
            structs[item.__name__] = item
    
    return structs


if __name__ == '__main__':
    load_structs_from_path("structs.py")