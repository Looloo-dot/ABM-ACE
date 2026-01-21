from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np


@dataclass
class Household:
    """Household agent with adaptive behavior and climate exposure."""

    agent_id: int
    skill: float
    wealth: float
    risk_aversion: float
    green_adoption: float
    shock_exposure: float

    def decide_green_investment(
        self,
        social_signal: float,
        policy_subsidy: float,
        rng: np.random.Generator,
    ) -> float:
        """Return green investment share based on incentives and social norms."""
        base_propensity = 0.2 + 0.4 * self.skill
        social_component = 0.3 * social_signal
        subsidy_component = 0.4 * policy_subsidy
        noise = rng.normal(0, 0.03)
        decision = base_propensity + social_component + subsidy_component + noise
        return float(np.clip(decision, 0.0, 1.0))

    def update_wealth(self, income: float, climate_damage: float) -> None:
        """Update wealth after income and damages."""
        self.wealth = max(0.0, self.wealth + income - climate_damage)


@dataclass
class Firm:
    """Firm agent producing output and deciding on green upgrades."""

    firm_id: int
    productivity: float
    green_capital: float
    emissions_intensity: float

    def decide_green_upgrade(
        self, policy_subsidy: float, rng: np.random.Generator
    ) -> float:
        """Return investment share into green capital."""
        base = 0.15 + 0.2 * self.productivity
        subsidy = 0.4 * policy_subsidy
        noise = rng.normal(0, 0.02)
        decision = base + subsidy + noise
        return float(np.clip(decision, 0.0, 1.0))

    def update_emissions(self) -> None:
        """Update emissions intensity based on green capital."""
        self.emissions_intensity = max(0.1, 1.0 - self.green_capital)


def initialize_households(
    num_households: int,
    rng: np.random.Generator,
) -> Dict[int, Household]:
    """Initialize households with heterogeneity in skill and exposure."""
    households: Dict[int, Household] = {}
    skills = rng.beta(2, 3, size=num_households)
    exposures = rng.uniform(0.2, 0.8, size=num_households)
    for i in range(num_households):
        households[i] = Household(
            agent_id=i,
            skill=float(skills[i]),
            wealth=float(rng.uniform(0.5, 2.0)),
            risk_aversion=float(rng.uniform(0.3, 0.9)),
            green_adoption=float(rng.uniform(0.0, 0.2)),
            shock_exposure=float(exposures[i]),
        )
    return households


def initialize_firms(
    num_firms: int,
    rng: np.random.Generator,
) -> Dict[int, Firm]:
    """Initialize firms with heterogeneous productivity."""
    firms: Dict[int, Firm] = {}
    productivity = rng.beta(2.5, 2.0, size=num_firms)
    for i in range(num_firms):
        firms[i] = Firm(
            firm_id=i,
            productivity=float(productivity[i]),
            green_capital=float(rng.uniform(0.0, 0.3)),
            emissions_intensity=float(rng.uniform(0.7, 1.0)),
        )
    return firms
