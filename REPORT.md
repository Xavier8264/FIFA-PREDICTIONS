# 2026 FIFA World Cup — Championship Prediction

**Updated: July 5, 2026 (00:10 UTC)** — conditioned on the completed July 4
Round-of-16 results: **Morocco 3–0 Canada** and **France 1–0 Paraguay**
(Mbappé pen). Elo ratings refreshed post-match. Six R16 ties remain
unplayed; QF1 is now set: **Morocco v France** (Foxborough, July 9).

## Headline result

**France is now the most likely champion at 24.0%**, ahead of **Argentina
(19.9%)** and **Spain (15.2%)**. France overtook Argentina by banking its
Round-of-16 win: it is the only top seed already through to the
quarterfinals, with a favourable tie against Morocco next.

| # | Team | Reach QF | Reach SF | Reach Final | **Champion** |
|---|------|--------:|---------:|------------:|-------------:|
| 1 | France 🇫🇷 | ✅ 100% | 69.8% | 41.2% | **24.0%** |
| 2 | Argentina 🇦🇷 | 83.9% | 55.8% | 35.3% | **19.9%** |
| 3 | Spain 🇪🇸 | 62.4% | 44.8% | 25.5% | **15.2%** |
| 4 | Brazil 🇧🇷 | 60.6% | 31.7% | 15.1% | **7.0%** |
| 5 | England 🏴 | 51.4% | 28.8% | 14.3% | **6.8%** |
| 6 | Portugal 🇵🇹 | 37.6% | 22.6% | 10.1% | **4.8%** |
| 7 | Colombia 🇨🇴 | 55.6% | 23.2% | 11.3% | **4.8%** |
| 8 | Morocco 🇲🇦 | ✅ 100% | 30.2% | 11.8% | **4.5%** |
| 9 | Mexico 🇲🇽 | 48.6% | 23.0% | 9.5% | **3.7%** |
| 10 | Switzerland 🇨🇭 | 44.4% | 16.2% | 7.1% | **2.6%** |
| 11 | Belgium 🇧🇪 | 52.2% | 17.6% | 6.3% | **2.4%** |
| 12 | Norway 🇳🇴 | 39.4% | 16.5% | 6.2% | **2.2%** |
| 13 | United States 🇺🇸 | 47.8% | 15.1% | 5.2% | **1.9%** |
| 14 | Egypt 🇪🇬 | 16.1% | 4.8% | 1.3% | **0.3%** |
| — | Canada 🇨🇦 | eliminated | — | — | 0% |
| — | Paraguay 🇵🇾 | eliminated | — | — | 0% |

*(Initial July 4 pre-R16 run: Argentina 20.4%, France 19.6%, Spain 16.5% —
France's result flipped the order.)*

## Why France leads now

- France is the only contender with its quarterfinal place **already
  secured**, and its QF opponent (Morocco, blend 1925) is the softest draw
  any top-four side can get at this stage.
- **Spain** still faces Portugal in the R16, then likely a home-crowd USA in
  Los Angeles, then probably France in SF1 — three heavyweight fights before
  the final.
- **Argentina** keeps the softest R16 (Egypt) and a Switzerland/Colombia QF,
  but hasn't banked those wins yet; it still leads the bottom half easily.
- Mexico–England at the Azteca remains the closest remaining R16 tie
  (51.4/48.6 England after Mexico's +100 home-Elo).

## The bracket (after July 4)

```
TOP HALF                                BOTTOM HALF
QF1: Morocco – France       (set)       R16: Brazil – Norway     (E. Rutherford)
R16: Portugal – Spain   (Dallas)        R16: Mexico – England    (Azteca)
R16: USA – Belgium      (Seattle)       R16: Argentina – Egypt   (Atlanta)
QF2: (POR/ESP) v (USA/BEL)  Los Angeles R16: Switzerland – Colombia (Vancouver)
                                        QF3: (BRA/NOR) v (MEX/ENG)  Miami
                                        QF4: (ARG/EGY) v (SUI/COL)  Kansas City
SF1: QF1 v QF2  Arlington               SF2: QF3 v QF4  Atlanta
                 FINAL: New Jersey, July 19
```

## Method

1. **Data (fetched live; Elo refreshed July 5 00:05 UTC):**
   - World Elo ratings (eloratings.net), updated through the July 4 R16
     results — the strongest single predictor of international results.
   - FIFA ranking points (June 2026 cycle).
   - Transfermarkt squad market values (2026 WC squads).
   - Structural/qualitative covariates: population (talent pool), registered
     players, football-culture prominence index, GDP per capita (investment
     capacity), and World Cup pedigree (titles/finals/semifinals).
2. **Fundamental-strength model:** ridge regression of live Elo on the
   structural covariates, fit by gradient descent run to numerical
   convergence (4,245 iterations, tolerance 1e-12). Strongest fundamental
   signals: FIFA points, culture prominence, registered-player base.
3. **Blended rating:** 0.8 × live Elo + 0.2 × fundamentals — Elo carries the
   in-tournament form; fundamentals regularize small-sample noise.
4. **Match engine:** Elo win expectancy mapped to a Poisson goal model so
   90-minute draws, extra time, and penalty shootouts are simulated
   explicitly (Paraguay and Morocco reached the R16 via shootouts —
   knockout football hinges on this mechanic).
5. **Home advantage:** +100 Elo on own soil (Mexico at the Azteca; USA in
   every remaining venue from the QFs onward), +25 for co-hosts playing in a
   partner host country.
6. **Conditioning on reality:** R16 ties already decided (`DECIDED` in
   `model.py`) are locked to their actual winners; only undecided matches
   are simulated.
7. **Monte Carlo, run to convergence:** the bracket was simulated in
   200,000-tournament batches and stopped only when the full championship
   probability vector moved by less than 0.05 percentage points across three
   consecutive batches AND the 99% confidence half-width on the favourite
   fell below 0.1pp. **Converged after 1,800,000 simulated tournaments.**

## Robustness

Sensitivity re-runs on the pre-conditioned (July 4 morning) bracket, each to
full convergence, varying the Elo/fundamentals blend (0.7–0.9), home
advantage (60–140 Elo), and scoring environment (2.2–3.0 goals/match), kept
the same leading trio in every scenario with Argentina/France within ~1pp of
each other — the France-first ordering after conditioning is driven by the
actual July 4 results, not by parameter choices.

**Bottom line: France lifts the trophy in ~1 of 4 simulated worlds and is
the single most likely champion; Argentina ~1 in 5; Spain ~1 in 6.5. The
top three still account for only 59% combined — a genuinely open
tournament with Brazil and England as live outsiders.**

## Sources

- [eloratings.net World.tsv](https://www.eloratings.net/World.tsv) (live Elo)
- [CBS Sports — R32 results & R16 matchups](https://www.cbssports.com/soccer/news/2026-fifa-world-cup-bracket-round-of-32-results-round-of-16-matchups-final/)
- [Sky Sports — bracket & route to final](https://www.skysports.com/football/news/11095/13556636/world-cup-2026-bracket-and-knockout-fixtures-whos-facing-who-in-the-last-32-and-route-to-final)
- [CNN — Morocco 3–0 Canada](https://www.cnn.com/2026/07/04/sport/round-of-16-canada-morocco-paraguay-france)
- [ESPN — Mbappé penalty beats Paraguay](https://www.espn.com/soccer/story/_/id/49271796/kylian-mbappe-penalty-leads-france-paraguay-world-cup)
- [Planet Football — 2026 squads by market value](https://www.planetfootball.com/lists-and-rankings/world-cup-2026-every-squad-ranked-market-value)
- [football-ranking.com — FIFA points](https://football-ranking.com/fifa-world-rankings)
- [ESPN — FIFA rankings June 2026](https://www.espn.com/soccer/story/_/id/46664763/fifa-mens-top-50-world-rankings)
