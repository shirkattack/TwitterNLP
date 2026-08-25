"""Train one spaCy pipeline with hyperparameters supplied by a W&B sweep agent.

This script is the ``command`` executed by a sweep defined in
``corpus/sweep_bayes.yml``: W&B populates ``wandb.config`` with dotted keys
(e.g. ``training.dropout``) which are merged over the base spaCy config.

Usage (normally invoked by ``wandb agent``):
    python scripts/sweep_from_config.py corpus/gpu_config.cfg training --gpu-id 0
"""
from pathlib import Path

import typer
import wandb
from spacy import util
from spacy.cli._util import setup_gpu
from spacy.training.initialize import init_nlp
from spacy.training.loop import train
from thinc.api import Config


def train_from_config(default_config: Path, output_path: Path, gpu_id: int = -1) -> None:
    """Merge the active W&B run's config into ``default_config`` and train."""
    setup_gpu(gpu_id)
    loaded_local_config = util.load_config(default_config)
    with wandb.init() as run:
        sweeps_config = Config(util.dot_to_dict(dict(run.config)))
        merged_config = Config(loaded_local_config).merge(sweeps_config)
        nlp = init_nlp(merged_config)
        output_path.mkdir(parents=True, exist_ok=True)
        train(nlp, output_path, use_gpu=gpu_id)


def main(
    default_config: Path = typer.Argument(..., exists=True, dir_okay=False),
    output_path: Path = typer.Argument(..., file_okay=False),
    gpu_id: int = typer.Option(-1, help="GPU device id, or -1 for CPU"),
) -> None:
    train_from_config(default_config, output_path, gpu_id)


if __name__ == "__main__":
    typer.run(main)
