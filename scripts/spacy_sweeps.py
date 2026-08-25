"""Launch a Bayesian W&B hyperparameter sweep over a spaCy textcat config.

Usage:
    python scripts/spacy_sweeps.py corpus/gpu_config.cfg training --gpu-id 0 --count 20
"""
from pathlib import Path

import typer
import wandb

from sweep_from_config import train_from_config

SWEEP_PARAMETERS = {
    "training.dropout": {"min": 0.05, "max": 0.5},
    "training.optimizer.learn_rate": {"min": 0.001, "max": 0.01},
    "components.textcat.model.ngram_size": {"values": [1, 2, 3]},
    "components.textcat.model.conv_depth": {"values": [2, 3, 4]},
}


def main(
    default_config: Path = typer.Argument(..., exists=True, dir_okay=False),
    output_path: Path = typer.Argument(..., file_okay=False),
    project: str = typer.Option("twitter_textcat", help="W&B project name"),
    count: int = typer.Option(20, min=1, help="Number of sweep runs to execute"),
    gpu_id: int = typer.Option(-1, help="GPU device id, or -1 for CPU"),
) -> None:
    sweep_config = {
        "method": "bayes",
        "metric": {"name": "cats_macro_auc", "goal": "maximize"},
        "parameters": SWEEP_PARAMETERS,
    }
    sweep_id = wandb.sweep(sweep_config, project=project)
    wandb.agent(
        sweep_id,
        lambda: train_from_config(default_config, output_path, gpu_id),
        count=count,
    )


if __name__ == "__main__":
    typer.run(main)
