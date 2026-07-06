# FIFA-PREDICTIONS

Convergence-based Monte Carlo prediction model for the 2026 FIFA World Cup.

**➡️ See [REPORT.md](REPORT.md) for the headline prediction (generated
July 4, 2026, from the live Round-of-16 bracket).**

## Contents

- `data/teams.csv` — feature table for the 16 surviving teams: live Elo
  (post–Round of 32), FIFA points, Transfermarkt squad market value,
  population, GDP per capita, registered players, football-culture index,
  World Cup pedigree, host status.
- `model.py` — full pipeline: fundamentals ridge regression (gradient
  descent to convergence) → blended team strength → Poisson match engine
  with extra time/penalties and venue-based home advantage → batched Monte
  Carlo of the real bracket that stops only when championship probabilities
  converge.
- `results.csv` — converged round-by-round advancement probabilities.
- `REPORT.md` — methodology, results, sensitivity analysis, sources.

## Run

```bash
pip install numpy
python3 model.py
```

Runtime is a few seconds; the simulation stops automatically at its
convergence criterion (1.6M simulated tournaments at the default seed).
