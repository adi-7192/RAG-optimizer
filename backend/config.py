import yaml
import os
from typing import List, Dict
from .models import PipelineConfig

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs", "pipelines.yaml")

def load_pipeline_configs() -> Dict[str, PipelineConfig]:
    if not os.path.exists(CONFIG_PATH):
        return {}
    
    with open(CONFIG_PATH, "r") as f:
        data = yaml.safe_load(f)
    
    configs = {}
    for p in data.get("pipelines", []):
        config = PipelineConfig(**p)
        configs[config.name] = config
    return configs

def get_pipeline_config(name: str) -> PipelineConfig:
    configs = load_pipeline_configs()
    return configs.get(name)
