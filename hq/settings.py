import os
import sys
import appdirs
import importlib
import importlib.util

from pathlib import Path

def get_config_file_path():
    return "/hq/config/__init__.py"

def get_config_dir():
    mvar = os.environ.get('MY_CONFIG')
    if mvar is not None:
        mycfg_dir = Path(mvar)
    else:
        mycfg_dir = Path(appdirs.user_config_dir('hq'))
    return mycfg_dir

def import_file(module_name, full_path):
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

def setup_config():
    config_dir = get_config_dir()

    if not config_dir.exists():
        print("Couldn't find config dir")
        return

    mpath = str(config_dir)
    full_path = mpath + get_config_file_path()
    import_file("hq.config", full_path)
