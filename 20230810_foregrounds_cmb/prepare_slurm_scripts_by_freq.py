from pathlib import Path
import sys
import subprocess

folder = Path(f"jobs")
folder.mkdir(exist_ok=True, parents=True)

from glob import glob
sims = list(glob("*.toml"))
sims = [s.split(".")[0] for s in sims]
sims.remove("common")

from mapsims.channel_utils import parse_channels

import toml
config = toml.load("common.toml")

chs = parse_channels(instrument_parameters=config["instrument_parameters"])
for simulation_type in sims:
    config_file = simulation_type
    template = open("submit.slurm").read()
    hours = 24
    minutes = 00
    for channel in chs:
        tag = channel.tag.replace(" ", "_")
        filename = f"job_{simulation_type}_{tag}.slurm"
        with open(folder / filename, "w") as f:
            print(f"sbatch jobs/{filename} &")
            f.write(
                template.format(
                    simulation_type=simulation_type,
                    hours=hours,
                    minutes=minutes,
                    channels=tag,
                    run_channels=tag,
                    config_file=config_file,
                )
            )

        subprocess.run(["sbatch", f"jobs/{filename}"])
