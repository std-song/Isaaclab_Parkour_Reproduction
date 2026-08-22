"""Terrain-only evaluation variants for supplementary robustness experiments."""

from __future__ import annotations

from typing import Any


EXPERIMENTS: dict[str, dict[str, Any]] = {
    "hurdle_base": {
        "terrain": "parkour_hurdle",
        "hurdle_height_range": "0.1+0.1*difficulty, 0.15+0.25*difficulty",
        "half_valid_width": (0.4, 0.8),
        "x_range": (1.2, 2.2),
    },
    "hurdle_medium": {
        "terrain": "parkour_hurdle",
        "hurdle_height_range": "0.15+0.15*difficulty, 0.25+0.25*difficulty",
        "half_valid_width": (0.35, 0.65),
        "x_range": (1.0, 1.8),
    },
    "hurdle_hard": {
        "terrain": "parkour_hurdle",
        "hurdle_height_range": "0.2+0.2*difficulty, 0.3+0.3*difficulty",
        "half_valid_width": (0.3, 0.5),
        "x_range": (0.8, 1.5),
    },
    "step_base": {
        "terrain": "parkour_step",
        "step_height": "0.1 + 0.35*difficulty",
        "continuous_steps": 3,
    },
    "step_medium": {
        "terrain": "parkour_step",
        "step_height": "0.15 + 0.35*difficulty",
        "continuous_steps": 4,
    },
    "step_hard": {
        "terrain": "parkour_step",
        "step_height": "0.2 + 0.35*difficulty",
        "continuous_steps": 5,
    },
    "gap_base": {
        "terrain": "parkour_gap",
        "gap_size": "0.1 + 0.7*difficulty",
    },
    "gap_medium": {
        "terrain": "parkour_gap",
        "gap_size": "0.3 + 0.7*difficulty",
    },
    "gap_hard": {
        "terrain": "parkour_gap",
        "gap_size": "0.5 + 0.7*difficulty",
    },
    "beam_base": {
        "terrain": "parkour_beam",
        "beam_width": 1.0,
    },
    "beam_medium": {
        "terrain": "parkour_beam",
        "beam_width": 0.75,
    },
    "beam_hard": {
        "terrain": "parkour_beam",
        "beam_width": 0.5,
    },
}


def apply_terrain_experiment(env_cfg, experiment_name: str) -> dict[str, Any]:
    """Restrict evaluation to one terrain type and apply one parameter level."""
    experiment = EXPERIMENTS[experiment_name]
    generator_cfg = env_cfg.scene.terrain.terrain_generator
    target_name = experiment["terrain"]

    for name, sub_terrain in generator_cfg.sub_terrains.items():
        sub_terrain.proportion = 1.0 if name == target_name else 0.0

    target_cfg = generator_cfg.sub_terrains[target_name]
    for key, value in experiment.items():
        if key != "terrain":
            setattr(target_cfg, key, value)

    generator_cfg.random_difficulty = True
    generator_cfg.difficulty_range = (0.0, 1.0)
    generator_cfg.use_cache = False
    return experiment.copy()
