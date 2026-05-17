import importlib
import sys
from pathlib import Path
from core.base_node import BaseNode


def load_all_nodes(config=None, nodes_folder=None):

    factory = {}

    if nodes_folder is not None:
        scan_directory(nodes_folder, factory)
    else:
        scan_directory(Path("nodes"), factory)

    if config and config.custom_nodes_dir:
        custom_dir = Path(config.custom_nodes_dir)
        if custom_dir.is_dir():
            scan_directory(custom_dir, factory)

    groups = {}
    for name, cls in factory.items():
        grp = getattr(cls, "group", "Ungrouped")
        groups.setdefault(grp, []).append(name)
    return factory, groups


def scan_directory(directory: Path, factory):
    if not directory.is_dir():
        return
    sys.path.insert(0, str(directory.resolve()))
    for py_file in directory.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
        module_name = py_file.stem
        try:
            mod = importlib.import_module(module_name)
            for attr in dir(mod):
                obj = getattr(mod, attr)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, BaseNode)
                    and obj is not BaseNode
                ):
                    register_node_class(obj, factory)
        except Exception as e:
            print(f"Failed to load {module_name}: {e}")


def register_node_class(cls, factory):
    if cls.__name__ not in factory:
        factory[cls.__name__] = cls
