# Contributing to ABM-ACE

Thanks for your interest in contributing! We welcome research ideas, model
extensions, documentation improvements, and reproducibility enhancements.

## Ground Rules

- Be respectful and follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Open an issue before large changes so we can coordinate direction.
- Prefer small, well-scoped pull requests with clear rationale.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Model

```bash
python -m abm_ace.run --steps 200 --seed 42
```

## Style & Quality

- Use clear, descriptive variable names.
- Document assumptions and parameters in code comments or docstrings.
- Keep functions small and testable.
- Add or update metrics when you introduce new dynamics.

## Reporting Issues

Please include:

- A short description of expected vs. actual behavior.
- Steps to reproduce (including CLI arguments).
- Any relevant logs or stack traces.

## Research Transparency

When adding new mechanisms, include:

- The conceptual motivation.
- A brief note on potential limitations or biases.
- Any references to literature or prior models.
