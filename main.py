import time

from datetime import timedelta
from pathlib import Path

import hydra

from omegaconf import DictConfig, OmegaConf
from omegaconf.omegaconf import open_dict

from src.utils.omegaconf import register_resolvers

def run_local(cfg: DictConfig):

    start_time = time.time()
    print(f"Starting application at {start_time}")
    
    # Resolve the config (project resolvers: not, equal, ifelse).
    register_resolvers()
    OmegaConf.resolve(cfg)

    # Get yaml names.
    hydra_cfg = hydra.core.hydra_config.HydraConfig.get()
    cfg_choice = OmegaConf.to_container(hydra_cfg.runtime.choices)

    # Apply Hydra config-group choices for every group defined in configurations/
    with open_dict(cfg):
        for group_key, choice in cfg_choice.items():
            if choice is not None and group_key in cfg:
                cfg[group_key]._name = choice
    
    
    # Set up the output directory (Hydra output dir + run name from +name=...).
    output_dir = Path(hydra_cfg.runtime.output_dir) 
    with open_dict(cfg):
        if "application" in cfg:
            cfg.application.output_dir = output_dir

    # Print the resolved config.
    print(OmegaConf.to_yaml(cfg))

    # Print the output directory.
    print(f"Output directory: {output_dir}")

    # Print the application name.
    print(f"Application name: {cfg.application._name}")

    # Print the project agent config name.
    print(f"Project agent: {cfg.project_agent._name}")

    # Print the module agent config name.
    print(f"Module agent: {cfg.module_agent._name}")

    # Print the task agent config name.
    print(f"Task agent: {cfg.task_agent._name}")
    
@hydra.main(version_base=None, config_path="configurations", config_name="config")
def run(cfg: DictConfig):
    if "name" not in cfg:
        raise ValueError(
            "Must specify a name for the run with command line argument '+name=[name]'"
        )


    run_local(cfg)


if __name__ == "__main__":
    run()