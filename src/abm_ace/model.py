from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import networkx as nx
import numpy as np

from abm_ace.agents import Firm, Household, initialize_firms, initialize_households
from abm_ace.metrics import Metrics, gini_coefficient, resilience_index


@dataclass
class Policy:
    """Policy levers for the simulation."""

    green_subsidy: float
    progressive_tax: float
    targeted_transfer: float


@dataclass
class ModelConfig:
    """Configuration for the ABM simulation."""

    num_households: int = 200
    num_firms: int = 40
    shock_probability: float = 0.1
    shock_severity: float = 0.4
    network_rewire_prob: float = 0.02


class ABMModel:
    """Adaptive climate-economy ABM with social influence."""

    def __init__(self, config: ModelConfig, policy: Policy, seed: int = 42) -> None:
        self.config = config
        self.policy = policy
        self.rng = np.random.default_rng(seed)
        self.households = initialize_households(config.num_households, self.rng)
        self.firms = initialize_firms(config.num_firms, self.rng)
        self.network = self._initialize_network(config.num_households)
        self.output_history: List[float] = []
        self.emissions_history: List[float] = []

    def _initialize_network(self, num_households: int) -> nx.Graph:
        """Initialize a small-world social network for influence dynamics."""
        graph = nx.watts_strogatz_graph(num_households, k=6, p=0.1, seed=1)
        return graph

    def _apply_climate_shock(self) -> float:
        """Return a shock multiplier for productivity and wealth."""
        if self.rng.random() < self.config.shock_probability:
            return 1.0 - self.config.shock_severity
        return 1.0

    def _social_signal(self, household_id: int) -> float:
        """Average green adoption of neighbors for social influence."""
        neighbors = list(self.network.neighbors(household_id))
        if not neighbors:
            return 0.0
        return float(np.mean([self.households[n].green_adoption for n in neighbors]))

    def step(self, step_id: int) -> Metrics:
        """Advance the model by one time step and return metrics."""
        shock_multiplier = self._apply_climate_shock()
        total_output = 0.0
        total_emissions = 0.0

        for firm in self.firms.values():
            investment_share = firm.decide_green_upgrade(self.policy.green_subsidy, self.rng)
            firm.green_capital = np.clip(firm.green_capital + 0.1 * investment_share, 0.0, 1.0)
            firm.update_emissions()
            output = firm.productivity * shock_multiplier
            total_output += output
            total_emissions += output * firm.emissions_intensity

        outputs_per_household = total_output / len(self.households)
        for household in self.households.values():
            social_signal = self._social_signal(household.agent_id)
            green_investment = household.decide_green_investment(
                social_signal, self.policy.green_subsidy, self.rng
            )
            household.green_adoption = np.clip(
                household.green_adoption + 0.05 * green_investment, 0.0, 1.0
            )
            climate_damage = household.shock_exposure * (1.0 - shock_multiplier)
            progressive_tax = self.policy.progressive_tax * max(0.0, household.wealth - 1.0)
            transfer = self.policy.targeted_transfer * (1.0 - household.wealth)
            income = outputs_per_household * (0.8 + household.skill)
            household.update_wealth(income - progressive_tax + transfer, climate_damage)

        if self.rng.random() < self.config.network_rewire_prob:
            self._rewire_network()

        avg_wealth = float(np.mean([h.wealth for h in self.households.values()]))
        gini = gini_coefficient(np.array([h.wealth for h in self.households.values()]))
        green_adoption = float(np.mean([h.green_adoption for h in self.households.values()]))
        emissions = total_emissions / max(total_output, 1e-6)

        self.output_history.append(total_output)
        self.emissions_history.append(emissions)

        metrics = Metrics(
            step=step_id,
            avg_wealth=avg_wealth,
            gini=gini,
            green_adoption=green_adoption,
            emissions=emissions,
            resilience=resilience_index(self.output_history),
        )
        return metrics

    def _rewire_network(self) -> None:
        """Rewire a random edge to simulate network adaptation."""
        if self.network.number_of_edges() == 0:
            return
        edge = list(self.network.edges())[self.rng.integers(0, self.network.number_of_edges())]
        self.network.remove_edge(*edge)
        node = self.rng.integers(0, self.config.num_households)
        target = self.rng.integers(0, self.config.num_households)
        if node != target:
            self.network.add_edge(int(node), int(target))

    def run(self, steps: int) -> List[Metrics]:
        """Run the model for a given number of steps."""
        metrics: List[Metrics] = []
        for step_id in range(steps):
            metrics.append(self.step(step_id))
        return metrics
