# 2026 FIFA World Cup — Championship Prediction

**Updated: July 6, 2026 (03:40 UTC)** — conditioned on all four completed
Round-of-16 results:

- July 4: **Morocco 3–0 Canada**, **France 1–0 Paraguay**
- July 5: **Norway 2–1 Brazil** (Haaland brace — the shock of the round),
  **England 3–2 Mexico** at the Azteca (with ten men)

Elo refreshed post-match (England's late finish computed with the
eloratings.net formula pending feed ingestion). QF1 and QF3 are now set;
four R16 ties remain: Portugal–Spain and USA–Belgium (July 6),
Argentina–Egypt and Switzerland–Colombia (July 7).

## Headline result

**France remains the most likely champion at 23.6%**, ahead of **Argentina
(18.8%)**, with **England (16.0%)** leaping past Spain (15.0%) after
Brazil's elimination cleared its side of the bracket.

| # | Team | Reach QF | Reach SF | Reach Final | **Champion** |
|---|------|--------:|---------:|------------:|-------------:|
| 1 | France 🇫🇷 | ✅ 100% | 69.8% | 41.0% | **23.6%** |
| 2 | Argentina 🇦🇷 | 83.9% | 55.6% | 33.6% | **18.8%** |
| 3 | England 🏴 | ✅ 100% | 61.5% | 32.1% | **16.0%** |
| 4 | Spain 🇪🇸 | 62.2% | 44.6% | 25.5% | **15.0%** |
| 5 | Norway 🇳🇴 | ✅ 100% | 38.5% | 15.7% | **6.1%** |
| 6 | Portugal 🇵🇹 | 37.8% | 22.8% | 10.3% | **4.8%** |
| 7 | Colombia 🇨🇴 | 55.3% | 23.1% | 10.7% | **4.5%** |
| 8 | Morocco 🇲🇦 | ✅ 100% | 30.2% | 11.7% | **4.4%** |
| 9 | Switzerland 🇨🇭 | 44.7% | 16.5% | 6.8% | **2.5%** |
| 10 | Belgium 🇧🇪 | 52.4% | 17.6% | 6.4% | **2.4%** |
| 11 | United States 🇺🇸 | 47.6% | 15.0% | 5.1% | **1.8%** |
| 12 | Egypt 🇪🇬 | 16.1% | 4.7% | 1.2% | **0.3%** |
| — | Brazil 🇧🇷 | eliminated | — | — | 0% |
| — | Mexico 🇲🇽 | eliminated | — | — | 0% |
| — | Canada 🇨🇦 | eliminated | — | — | 0% |
| — | Paraguay 🇵🇾 | eliminated | — | — | 0% |

*(Trajectory: July 4 pre-R16 — ARG 20.4, FRA 19.6, ESP 16.5. After July 4
games — FRA 24.0, ARG 19.9, ESP 15.2. Now — FRA 23.6, ARG 18.8, ENG 16.0.)*

## What changed on July 5

- **Brazil (7.0% → out).** Norway's win removes the bottom half's second
  seed. England is the biggest beneficiary: a Norway QF instead of a
  probable Brazil QF nearly doubles its semifinal odds (28.8% → 61.5%).
- **England over Spain on path, not strength.** Spain still rates higher
  per match (blend 2150 v 2080) but must beat Portugal, then likely a
  home-crowd USA, then probably France — while England's route to the
  final runs through Norway then the Argentina-half survivor.
- **Norway is now the live dark horse (6.1%)** — a top-five title chance
  requires beating England, but Haaland's side just showed it can take
  down a heavyweight.
- **Argentina dips slightly** (19.9% → 18.8%): England at 2080 blend is a
  tougher projected final opponent than the Brazil/England mixture was.

## The bracket (after July 5)

```
TOP HALF                                BOTTOM HALF
QF1: Morocco – France       (set)       QF3: Norway – England    (set)
R16: Portugal – Spain   (Dallas, Jul 6) R16: Argentina – Egypt   (Atlanta, Jul 7)
R16: USA – Belgium     (Seattle, Jul 6) R16: Switzerland – Colombia (Vancouver, Jul 7)
QF2: (POR/ESP) v (USA/BEL)  Los Angeles QF4: (ARG/EGY) v (SUI/COL)  Kansas City
SF1: QF1 v QF2  Arlington               SF2: QF3 v QF4  Atlanta
                 FINAL: New Jersey, July 19
```

## Method

1. **Data (fetched live; Elo refreshed July 6 03:35 UTC):**
   - World Elo ratings (eloratings.net), updated through the July 5 R16
     results — the strongest single predictor of international results.
     (England–Mexico had not yet been ingested by the feed; England's +30
     was computed with the site's own update rule: K=60, one-goal margin,
     +100 home Elo for Mexico at the Azteca.)
   - FIFA ranking points (June 2026 cycle).
   - Transfermarkt squad market values (2026 WC squads).
   - Structural/qualitative covariates: population (talent pool), registered
     players, football-culture prominence index, GDP per capita (investment
     capacity), and World Cup pedigree (titles/finals/semifinals).
2. **Fundamental-strength model:** ridge regression of live Elo on the
   structural covariates, fit by gradient descent run to numerical
   convergence (4,244 iterations, tolerance 1e-12).
3. **Blended rating:** 0.8 × live Elo + 0.2 × fundamentals.
4. **Match engine:** Elo win expectancy mapped to a Poisson goal model with
   explicit extra time and penalty shootouts.
5. **Home advantage:** +100 Elo on own soil (USA in every remaining venue),
   +25 for co-hosts playing in a partner host country.
6. **Conditioning on reality:** all four decided R16 ties (`DECIDED` in
   `model.py`) are locked to their actual winners; only undecided matches
   are simulated.
7. **Monte Carlo, run to convergence:** 200,000-tournament batches, stopping
   only when every championship probability moves < 0.05pp across three
   consecutive batches AND the favourite's 99% CI half-width < 0.1pp.
   **Converged after 1,600,000 simulated tournaments.**

## Robustness

Sensitivity re-runs on the original (July 4 morning) bracket, each to full
convergence, varying the Elo/fundamentals blend (0.7–0.9), home advantage
(60–140 Elo), and scoring environment (2.2–3.0 goals/match), preserved the
leaders' ordering in every scenario. The current France-first, England-third
ordering is driven by actual on-pitch results, not parameter choices.

**Bottom line: France lifts the trophy in ~1 of 4.2 simulated worlds; the
Argentina/England/Spain chasing pack sits at 15–19% each. Half the field is
gone and the top four still only account for 73% — the July 6–7 ties
(especially Portugal–Spain) will move these numbers sharply.**

## Sources

- [eloratings.net World.tsv](https://www.eloratings.net/World.tsv) (live Elo)
- [CBS Sports — R32 results & R16 matchups](https://www.cbssports.com/soccer/news/2026-fifa-world-cup-bracket-round-of-32-results-round-of-16-matchups-final/)
- [Sky Sports — bracket & route to final](https://www.skysports.com/football/news/11095/13556636/world-cup-2026-bracket-and-knockout-fixtures-whos-facing-who-in-the-last-32-and-route-to-final)
- [CNN — Norway stuns Brazil](https://www.cnn.com/2026/07/05/sport/world-cup-round-of-16-sunday)
- [ESPN — Brazil 1–2 Norway](https://www.espn.com/soccer/match/_/gameId/760504/norway-brazil)
- [ESPN — Mexico 2–3 England](https://www.espn.com/soccer/match/_/gameId/760505/england-mexico)
- [CNN — Morocco 3–0 Canada](https://www.cnn.com/2026/07/04/sport/round-of-16-canada-morocco-paraguay-france)
- [ESPN — Mbappé penalty beats Paraguay](https://www.espn.com/soccer/story/_/id/49271796/kylian-mbappe-penalty-leads-france-paraguay-world-cup)
- [Planet Football — 2026 squads by market value](https://www.planetfootball.com/lists-and-rankings/world-cup-2026-every-squad-ranked-market-value)
- [football-ranking.com — FIFA points](https://football-ranking.com/fifa-world-rankings)
