import json, os

here    = os.path.dirname(__file__)
cfgfile = os.path.join(here, "config.json")

with open(cfgfile) as f:
    data = json.load(f)

CONFIG_RD = data.get('config_rd')
CONFIG_ALPHA = data.get('alpha')

if not CONFIG_RD:
    raise RuntimeError(f"{cfgfile} is missing a 'config_rd' key")

if not CONFIG_ALPHA:
    raise RuntimeError(f"{cfgfile} is missing a 'alpha' key")
