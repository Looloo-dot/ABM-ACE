from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List

import numpy as np

from abm_ace.metrics import gini
from abm_ace.types import Firm, Household, Policy


class Economy:
    def __init__(
        self,
        households: List[Household],
        firms: List[Firm],
        policy: Policy,
        rng: np.random.Generator,
    ) -> None:
        self.households = households
        self.firms = firms
        self.policy = policy
        self.rng = rng
        self.time = 0

    def step(self) -> Dict[str, float]:
        shock = self._climate_shock()
        self._firm_adjustments(shock)
        self._labor_market()
        emissions = self._household_accounts(shock)
        metrics = self._metrics(emissions)
        self.time += 1
        return metrics

    def snapshot(self) -> Dict[str, float]:
        emissions = sum(f.emissions_intensity for f in self.firms if f.alive)
        return self._metrics(emissions)

    def _climate_shock(self) -> float:
        return self.rng.normal(0.0, 0.08)

    def _firm_adjustments(self, shock: float) -> None:
        for firm in self.firms:
            if not firm.alive:
                continue
            firm.productivity = max(0.2, firm.productivity * (1.0 - shock))
            firm.wage_offer = max(0.4, firm.wage_offer * (0.98 + 0.04 * firm.productivity))
            firm.hiring_rate = min(0.5, max(0.05, firm.hiring_rate * (1.0 - shock)))
            firm.emissions_intensity = max(0.1, firm.emissions_intensity * (0.97 + 0.05 * firm.productivity))
            if firm.productivity < 0.25:
                firm.alive = False

    def _labor_market(self) -> None:
        alive_firms = [f for f in self.firms if f.alive]
        if not alive_firms:
            for household in self.households:
                household.employed = False
            return

        wage_offers = np.array([f.wage_offer for f in alive_firms])
        total_jobs = sum(int(f.hiring_rate * len(self.households)) for f in alive_firms)
        total_jobs = max(1, min(total_jobs, len(self.households)))
        employed_ids = set(self.rng.choice(len(self.households), size=total_jobs, replace=False))

        for idx, household in enumerate(self.households):
            household.employed = idx in employed_ids
            if household.employed:
                wage = float(self.rng.choice(wage_offers))
                household.income = wage
            else:
                household.income = self.policy.safety_net

    def _household_accounts(self, shock: float) -> float:
        emissions = 0.0
        total_tax = 0.0
        for household in self.households:
            baseline = household.consumption_need * (1.0 - 0.5 * shock)
            consumption = max(0.2, baseline * (0.6 + 0.6 * household.risk_tolerance))
            income = household.income
            tax = self.policy.carbon_tax * consumption
            total_tax += tax
            household.wealth += income - consumption - tax
            emissions += consumption

        dividend = self.policy.dividend_share * total_tax / len(self.households)
        for household in self.households:
            household.wealth += dividend

        return emissions

    def _metrics(self, emissions: float) -> Dict[str, float]:
        incomes = [h.income for h in self.households]
        wealths = [h.wealth for h in self.households]
        consumption = [h.consumption_need for h in self.households]
        unemployed = sum(1 for h in self.households if not h.employed)
        alive_firms = sum(1 for f in self.firms if f.alive)

        return {
            "step": float(self.time),
            "households": float(len(self.households)),
            "firms": float(alive_firms),
            "gini": float(gini(wealths)),
            "unemployment": float(unemployed / len(self.households)),
            "avg_income": float(np.mean(incomes)),
            "avg_consumption_need": float(np.mean(consumption)),
            "emissions": float(emissions / len(self.households)),
        }


def build_economy(
    rng: np.random.Generator,
    households: int = 200,
    firms: int = 30,
) -> Economy:
    household_agents = []
    for i in range(households):
        household_agents.append(
            Household(
                household_id=i,
                wealth=float(rng.lognormal(mean=0.0, sigma=0.5)),
                income=1.0,
                consumption_need=float(rng.uniform(0.8, 1.2)),
                risk_tolerance=float(rng.uniform(0.3, 0.9)),
            )
        )

    firm_agents = []
    for i in range(firms):
        firm_agents.append(
            Firm(
                firm_id=i,
                productivity=float(rng.uniform(0.8, 1.3)),
                wage_offer=float(rng.uniform(0.9, 1.3)),
                hiring_rate=float(rng.uniform(0.08, 0.18)),
                emissions_intensity=float(rng.uniform(0.7, 1.2)),
            )
        )

    policy = Policy(carbon_tax=0.08, dividend_share=0.9, safety_net=0.5)
    return Economy(household_agents, firm_agents, policy, rng)


def model_config_summary(economy: Economy) -> Dict[str, float]:
    return {
        "policy": asdict(economy.policy),
        "households": len(economy.households),
        "firms": len(economy.firms),
    }
