import argparse, json, os

parser = argparse.ArgumentParser(
    description="Persist the config_rd value for later runs"
)
parser.add_argument(
    '--config_rd', type=str, required=True,
    help="Name of the config to use (e.g. resnik_n_all_…)"
)
parser.add_argument('--alpha', type=str, required=True)

args = parser.parse_args()

here     = os.path.dirname(__file__)
cfg_path = os.path.join(here, "config.json")


with open(cfg_path, "w") as f:
    json.dump({'config_rd': args.config_rd, 'alpha': args.alpha}, f, indent=2)

#print(f"Wrote config_rd={args.config_rd!r} → {cfg_path}")
