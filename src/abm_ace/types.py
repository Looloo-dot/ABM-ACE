from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Household:
    household_id: int
    wealth: float
    income: float
    consumption_need: float
    risk_tolerance: float
    employed: bool = True


@dataclass
class Firm:
    firm_id: int
    productivity: float
    wage_offer: float
    hiring_rate: float
    emissions_intensity: float
    alive: bool = True


@dataclass
class Policy:
    carbon_tax: float
    dividend_share: float
    safety_net: float
