# 2026 FIFA World Cup — Championship Prediction

**Updated: July 7, 2026 (00:15 UTC)** — conditioned on all six completed
Round-of-16 results:

- July 4: **Morocco 3–0 Canada**, **France 1–0 Paraguay**
- July 5: **Norway 2–1 Brazil** (Haaland brace), **England 3–2 Mexico**
  at the Azteca (with ten men)
- July 6: **Spain 1–0 Portugal** (Merino, 91' — Ronaldo's last World Cup
  game), **Belgium 4–1 USA** (De Ketelaere x2, Vanaken, Lukaku)

Elo refreshed post-match (Belgium/USA computed manually via the
eloratings.net K=60 formula, cross-validated against the feed's own
Spain/Portugal update, which matched to the point). **The entire top half
of the bracket is now set** — QF1 (Morocco–France) and QF2 (Spain–Belgium)
are both locked in. Two R16 ties remain: Argentina–Egypt and
Switzerland–Colombia (July 7).

## Headline result

**Spain has retaken the lead at 24.2%**, narrowly ahead of **France
(21.4%)** and **Argentina (18.1%)**, after eliminating Portugal and drawing
Belgium — the weakest remaining QF2 opponent — rather than the USA/France
gauntlet the bracket originally threatened.

| # | Team | Reach QF | Reach SF | Reach Final | **Champion** |
|---|------|--------:|---------:|------------:|-------------:|
| 1 | Spain 🇪🇸 | ✅ 100% | 69.1% | 40.4% | **24.2%** |
| 2 | France 🇫🇷 | ✅ 100% | 69.9% | 37.3% | **21.4%** |
| 3 | Argentina 🇦🇷 | 84.2% | 55.8% | 33.8% | **18.1%** |
| 4 | England 🏴 | ✅ 100% | 61.4% | 31.9% | **15.1%** |
| 5 | Norway 🇳🇴 | ✅ 100% | 38.6% | 15.7% | **5.7%** |
| 6 | Belgium 🇧🇪 | ✅ 100% | 30.9% | 12.2% | **4.9%** |
| 7 | Colombia 🇨🇴 | 55.3% | 23.0% | 10.7% | **4.2%** |
| 8 | Morocco 🇲🇦 | ✅ 100% | 30.1% | 10.2% | **3.8%** |
| 9 | Switzerland 🇨🇭 | 44.7% | 16.5% | 6.8% | **2.4%** |
| 10 | Egypt 🇪🇬 | 15.8% | 4.7% | 1.1% | **0.2%** |
| — | Brazil, Canada, Mexico, Paraguay, Portugal, USA | eliminated | — | — | 0% |

*(Trajectory: pre-R16 ARG 20.4/FRA 19.6/ESP 16.5 → post-Jul 4 FRA 24.0/ARG
19.9/ESP 15.2 → post-Jul 5 FRA 23.6/ARG 18.8/ENG 16.0/ESP 15.0 → now ESP
24.2/FRA 21.4/ARG 18.1/ENG 15.1.)*

## Why Spain jumped back to #1

- **Spain's toughest remaining obstacle just disappeared.** Portugal is
  out, and Belgium — a 100% underdog in the model against Spain (78%
  France beat Belgium in the earlier simulation, similarly Spain now
  faces a team it's favored against by a wide margin at every stage) —
  replaces what would have been a likely Spain–France semifinal collision
  one round earlier than expected.
- **France's path got no harder** (still Morocco in the QF) but its
  semifinal opponent is now confirmed as the Spain/Belgium winner, i.e.
  Spain is very likely (69% within that pairing) — so France's title odds
  actually *dropped* (24.0% → 21.4%) purely because the great unknown
  ("whoever survives Portugal/Spain/USA/Belgium") resolved toward the
  stronger possible opponent.
- **Argentina** (18.1%) and **England** (15.1%) are unaffected in the
  bottom half — both already have their QFs and remain the second bracket
  half's top two.
- The **entire top half of the draw is now determined through the
  semifinal matchup**: it will be **Spain vs France in SF1**, barring an
  upset in either quarterfinal — a virtual rerun of Euro-era continental
  rivalries and the two heaviest-weighted teams in the whole model.

## The bracket (after July 6)

```
TOP HALF (fully set through SF1)         BOTTOM HALF
QF1: Morocco – France      (set)         QF3: Norway – England    (set)
QF2: Spain – Belgium       (set)         R16: Argentina – Egypt   (Atlanta, Jul 7)
                                          R16: Switzerland – Colombia (Vancouver, Jul 7)
                                          QF4: (ARG/EGY) v (SUI/COL)  Kansas City
SF1: QF1 v QF2  Arlington                SF2: QF3 v QF4  Atlanta
                 FINAL: New Jersey, July 19
```

## Method

1. **Data (fetched live; Elo refreshed July 7 00:10 UTC):**
   - World Elo ratings (eloratings.net), updated through the July 6 R16
     results. Spain/Portugal already reflected in the live feed (2177/1995
     — this was cross-checked against a manual K=60 recomputation and
     matched exactly, validating the method); Belgium/USA computed manually
     with the same formula since the feed hadn't yet ingested the Seattle
     result (USA home-field +100 in the expectation term, goal-difference
     weight G=1.375 for the 3-goal margin → Belgium 1950, USA 1758).
   - FIFA ranking points (June 2026 cycle), Transfermarkt squad market
     values, and the structural/qualitative covariates used throughout
     (population, registered players, culture-prominence index, GDP per
     capita, World Cup pedigree).
2. **Fundamental-strength model:** ridge regression of live Elo on the
   structural covariates, fit by gradient descent to convergence (4,272
   iterations, tolerance 1e-12).
3. **Blended rating:** 0.8 × live Elo + 0.2 × fundamentals.
4. **Match engine:** Elo win expectancy → Poisson goal model with explicit
   extra time and penalty shootouts.
5. **Home advantage:** +100 Elo on own soil, +25 for co-hosts in a partner
   host country (moot from the QFs on — all remaining venues are U.S. soil
   except none of the surviving teams are Mexico/Canada).
6. **Conditioning on reality:** all six decided R16 ties (`DECIDED` in
   `model.py`) are locked to their actual winners; only the two remaining
   R16 matches are simulated, alongside every subsequent round.
7. **Monte Carlo, run to convergence:** 200,000-tournament batches,
   stopping only when every championship probability moves < 0.05pp across
   three consecutive batches AND the favourite's 99% CI half-width < 0.1pp.
   **Converged after 1,800,000 simulated tournaments.**

## Robustness

Sensitivity re-runs on the original (July 4 morning) bracket, each to full
convergence, varying the Elo/fundamentals blend (0.7–0.9), home advantage
(60–140 Elo), and scoring environment (2.2–3.0 goals/match), preserved the
same leading trio's ordering in every scenario. Since then the ordering has
moved twice — first to France, now to Spain — entirely because of real
results on the pitch, not parameter choices.

**Bottom line: with the top half of the bracket fully resolved through the
semifinal, Spain lifts the trophy in ~1 of 4.1 simulated worlds, France in
~1 of 4.7, Argentina in ~1 of 5.5. The bottom half (Argentina vs. the
Norway/England survivor) is still two matches away from being fully
determined — tomorrow's Argentina–Egypt and Switzerland–Colombia games are
the last pieces before every quarterfinal is locked in.**

## Sources

- [eloratings.net World.tsv](https://www.eloratings.net/World.tsv) (live Elo)
- [ESPN — Spain 1–0 Portugal](https://www.espn.com/soccer/match/_/gameId/760506/spain-portugal)
- [CNN — Belgium 4–1 USA](https://www.cnn.com/2026/07/06/sport/live-news/usa-belgium-world-cup-score)
- [ESPN — Brazil 1–2 Norway](https://www.espn.com/soccer/match/_/gameId/760504/norway-brazil)
- [ESPN — Mexico 2–3 England](https://www.espn.com/soccer/match/_/gameId/760505/england-mexico)
- [CNN — Morocco 3–0 Canada](https://www.cnn.com/2026/07/04/sport/round-of-16-canada-morocco-paraguay-france)
- [ESPN — Mbappé penalty beats Paraguay](https://www.espn.com/soccer/story/_/id/49271796/kylian-mbappe-penalty-leads-france-paraguay-world-cup)
- [Planet Football — 2026 squads by market value](https://www.planetfootball.com/lists-and-rankings/world-cup-2026-every-squad-ranked-market-value)
- [football-ranking.com — FIFA points](https://football-ranking.com/fifa-world-rankings)
