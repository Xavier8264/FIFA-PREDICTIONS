#!/usr/bin/env python3
"""
2026 FIFA World Cup championship prediction model.

Pipeline
--------
1. Fundamental-strength model: ridge regression (fit by full-batch gradient
   descent, iterated to numerical convergence) of live Elo ratings on
   structural / cultural covariates: squad market value, FIFA ranking points,
   football-culture prominence, population, registered players, GDP per
   capita, and World Cup pedigree. This captures the "qualitative" signal
   (talent pool, investment, culture) and shrinks noisy Elo readings toward
   fundamentals.
2. Blended team strength: S = w_elo * Elo + (1 - w_elo) * fundamental fit.
   Live Elo (updated through the Round of 32) dominates because it is the
   best-validated single predictor of international match outcomes.
3. Match model: Elo win expectancy mapped to a bivariate Poisson goal model
   so 90-minute draws, extra time, and penalty shootouts are simulated
   explicitly (knockout football is decided by these mechanics).
4. Home advantage: +100 Elo for a match on a team's own soil (Mexico at the
   Azteca, USA anywhere in the tournament's US venues), +25 for a co-host
   playing inside a partner host country (Mexico/Canada in US venues).
5. Monte Carlo simulation of the real remaining bracket (Round of 16 onward,
   verified pairings), run in batches and stopped only when the championship
   probability vector converges: max absolute change < CONV_TOL across
   CONV_PATIENCE consecutive batch checkpoints AND the 99% CI half-width on
   the favourite's probability is below CI_TOL.

Bracket (verified 2026-07-04, all Round-of-16 fixtures unplayed):
  R16: CAN-MAR (Houston), PAR-FRA (Philadelphia), BRA-NOR (E. Rutherford),
       MEX-ENG (Mexico City/Azteca), POR-ESP (Dallas), USA-BEL (Seattle),
       ARG-EGY (Atlanta), SUI-COL (Vancouver)
  QF1 = W(CAN-MAR) v W(PAR-FRA)   [Foxborough]
  QF2 = W(POR-ESP) v W(USA-BEL)   [Los Angeles]
  QF3 = W(BRA-NOR) v W(MEX-ENG)   [Miami]
  QF4 = W(ARG-EGY) v W(SUI-COL)   [Kansas City]
  SF1 = QF1 v QF2 [Arlington];  SF2 = QF3 v QF4 [Atlanta]
  Final: New Jersey, July 19.
"""

import csv
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- data
def load_teams():
    teams = {}
    with open(os.path.join(HERE, "data", "teams.csv")) as f:
        for row in csv.DictReader(f):
            teams[row["code"]] = {
                "name": row["team"],
                "elo": float(row["elo_live"]),
                "fifa": float(row["fifa_points"]),
                "mv": float(row["market_value_meur"]),
                "pop": float(row["population_m"]),
                "gdp": float(row["gdp_per_capita_kusd"]),
                "reg": float(row["registered_players_m"]),
                "culture": float(row["culture_index"]),
                "titles": float(row["wc_titles"]),
                "finals_lost": float(row["wc_finals_lost"]),
                "semis": float(row["wc_semis"]),
                "host": row["host_status"],
            }
    return teams


# ------------------------------------------- stage 1: fundamentals fit
def fit_fundamentals(teams, ridge=1.0, lr=0.05, tol=1e-12, max_iter=2_000_000):
    """Ridge regression of live Elo on structural features, fit by gradient
    descent iterated until the coefficient vector stops moving (< tol)."""
    codes = sorted(teams)
    feats, y = [], []
    for c in codes:
        t = teams[c]
        pedigree = 4 * t["titles"] + 2 * t["finals_lost"] + t["semis"]
        feats.append([
            np.log(t["mv"]),        # squad market value (talent quality)
            t["fifa"],              # FIFA ranking points (medium-run results)
            t["culture"],           # football-culture prominence (qualitative)
            np.log(t["pop"]),       # talent-pool size
            np.log(t["reg"]),       # organised player base
            np.log(t["gdp"]),       # investment capacity
            pedigree,               # World Cup pedigree
        ])
        y.append(t["elo"])
    X = np.array(feats)
    y = np.array(y)
    Xm, Xs = X.mean(0), X.std(0)
    Xz = (X - Xm) / Xs
    ym, ys = y.mean(), y.std()
    yz = (y - ym) / ys

    n, p = Xz.shape
    w = np.zeros(p)
    b = 0.0
    it = 0
    while True:
        r = Xz @ w + b - yz
        gw = Xz.T @ r / n + ridge * w / n
        gb = r.mean()
        w_new = w - lr * gw
        b_new = b - lr * gb
        delta = max(np.max(np.abs(w_new - w)), abs(b_new - b))
        w, b = w_new, b_new
        it += 1
        if delta < tol:
            break
        if it >= max_iter:
            raise RuntimeError("fundamental fit failed to converge")
    pred = (Xz @ w + b) * ys + ym
    return codes, dict(zip(codes, pred)), w, it


# --------------------------------------------- stage 2: blended rating
W_ELO = 0.80  # live Elo carries most weight; fundamentals shrink the rest


def blended_strength(teams):
    codes, fund, w, iters = fit_fundamentals(teams)
    out = {}
    for c in codes:
        out[c] = W_ELO * teams[c]["elo"] + (1 - W_ELO) * fund[c]
    return out, fund, w, iters


# ----------------------------------------------------- match mechanics
HOME_FULL = 100.0   # own-country venue
HOME_CO = 25.0      # co-host playing in partner host country

# venue country by match id
R16 = [
    ("CAN", "MAR", "US"),   # Houston
    ("PAR", "FRA", "US"),   # Philadelphia
    ("BRA", "NOR", "US"),   # East Rutherford
    ("MEX", "ENG", "MX"),   # Estadio Azteca
    ("POR", "ESP", "US"),   # Dallas
    ("USA", "BEL", "US"),   # Seattle
    ("ARG", "EGY", "US"),   # Atlanta
    ("SUI", "COL", "CA"),   # Vancouver
]

# R16 ties already decided on the pitch: (team_a, team_b) -> winner.
# July 4: Morocco 3-0 Canada; France 1-0 Paraguay.
# July 5: Brazil 1-2 Norway; Mexico 2-3 England.
# July 6: Portugal 0-1 Spain; USA 1-4 Belgium.
DECIDED = {
    ("CAN", "MAR"): "MAR",
    ("PAR", "FRA"): "FRA",
    ("BRA", "NOR"): "NOR",
    ("MEX", "ENG"): "ENG",
    ("POR", "ESP"): "ESP",
    ("USA", "BEL"): "BEL",
}

QF_VENUES = ["US", "US", "US", "US"]      # Foxborough, LA, Miami, Kansas City
SF_VENUES = ["US", "US"]                  # Arlington, Atlanta
FINAL_VENUE = "US"                        # New Jersey

HOST_OF = {"USA": "US", "MEX": "MX", "CAN": "CA"}


def home_adj(code, venue_country):
    home = HOST_OF.get(code)
    if home is None:
        return 0.0
    if home == venue_country:
        return HOME_FULL
    if venue_country in ("US", "MX", "CA"):
        return HOME_CO
    return 0.0


def win_expectancy(d):
    return 1.0 / (1.0 + 10.0 ** (-d / 400.0))


TOTAL_GOALS = 2.6          # expected 90-minute goals in a WC knockout
MARGIN_PER_ELO = 1 / 280.0  # expected goal margin per Elo point


def match_lambdas(d):
    margin = np.clip(d * MARGIN_PER_ELO, -2.2, 2.2)
    la = (TOTAL_GOALS + margin) / 2.0
    lb = (TOTAL_GOALS - margin) / 2.0
    return max(la, 0.15), max(lb, 0.15)


def sim_knockout(rng, sa, sb, adj_a, adj_b, n):
    """Vectorised simulation of n knockout matches between strengths sa, sb.
    Returns boolean array: True where team A advances."""
    d = (sa + adj_a) - (sb + adj_b)
    la, lb = match_lambdas(d)
    ga = rng.poisson(la, n)
    gb = rng.poisson(lb, n)
    a_wins = ga > gb
    draws = ga == gb
    nd = draws.sum()
    if nd:
        # extra time: 30 minutes at the same scoring rates
        ea = rng.poisson(la / 3.0, nd)
        eb = rng.poisson(lb / 3.0, nd)
        et_a = ea > eb
        et_draw = ea == eb
        # penalties: slight edge to the stronger side
        p_pen = 0.5 + np.clip(d, -400, 400) / 8000.0
        pens = rng.random(nd) < p_pen
        a_wins[draws] = np.where(et_draw, pens, et_a)
    return a_wins


# ------------------------------------------------ stage 3: Monte Carlo
BATCH = 200_000
CONV_TOL = 5e-4        # 0.05 percentage points
CONV_PATIENCE = 3      # consecutive batch checkpoints under tolerance
CI_TOL = 1e-3          # 99% CI half-width on the favourite
MAX_SIMS = 100_000_000


def simulate(strength, seed=42):
    rng = np.random.default_rng(seed)
    codes = list(strength)
    idx = {c: i for i, c in enumerate(codes)}
    champ_counts = np.zeros(len(codes), dtype=np.int64)
    final_counts = np.zeros(len(codes), dtype=np.int64)
    sf_counts = np.zeros(len(codes), dtype=np.int64)
    qf_counts = np.zeros(len(codes), dtype=np.int64)

    prev = None
    stable = 0
    total = 0
    history = []

    while True:
        n = BATCH
        # R16 winners as integer team indices per sim
        r16w = []
        for a, b, venue in R16:
            winner = DECIDED.get((a, b))
            if winner is not None:
                r16w.append(np.full(n, idx[winner]))
                continue
            aw = sim_knockout(
                rng, strength[a], strength[b],
                home_adj(a, venue), home_adj(b, venue), n)
            r16w.append(np.where(aw, idx[a], idx[b]))
        for w_ in r16w:
            np.add.at(qf_counts, w_, 1)  # QF participation == R16 win

        def play(ia, ib, venue):
            sa = np.array([strength[codes[i]] for i in range(len(codes))])
            adj = np.array([home_adj(c, venue) for c in codes])
            d = (sa[ia] + adj[ia]) - (sa[ib] + adj[ib])
            la = np.clip((TOTAL_GOALS + np.clip(d * MARGIN_PER_ELO, -2.2, 2.2)) / 2, 0.15, None)
            lb = np.clip((TOTAL_GOALS - np.clip(d * MARGIN_PER_ELO, -2.2, 2.2)) / 2, 0.15, None)
            ga = rng.poisson(la)
            gb = rng.poisson(lb)
            aw = ga > gb
            draws = ga == gb
            nd = draws.sum()
            if nd:
                ea = rng.poisson(la[draws] / 3.0)
                eb = rng.poisson(lb[draws] / 3.0)
                et_a = ea > eb
                et_draw = ea == eb
                p_pen = 0.5 + np.clip(d[draws], -400, 400) / 8000.0
                pens = rng.random(nd) < p_pen
                aw[draws] = np.where(et_draw, pens, et_a)
            return np.where(aw, ia, ib)

        qf1 = play(r16w[0], r16w[1], "US")
        qf2 = play(r16w[4], r16w[5], "US")
        qf3 = play(r16w[2], r16w[3], "US")
        qf4 = play(r16w[6], r16w[7], "US")
        for w_ in (qf1, qf2, qf3, qf4):
            np.add.at(sf_counts, w_, 1)

        sf1 = play(qf1, qf2, "US")
        sf2 = play(qf3, qf4, "US")
        for w_ in (sf1, sf2):
            np.add.at(final_counts, w_, 1)

        champ = play(sf1, sf2, "US")
        np.add.at(champ_counts, champ, 1)

        total += n
        p = champ_counts / total
        history.append((total, p.copy()))
        if prev is not None:
            delta = np.max(np.abs(p - prev))
            pfav = p.max()
            ci = 2.576 * np.sqrt(pfav * (1 - pfav) / total)
            if delta < CONV_TOL and ci < CI_TOL:
                stable += 1
            else:
                stable = 0
            if stable >= CONV_PATIENCE:
                break
        prev = p.copy()
        if total >= MAX_SIMS:
            raise RuntimeError("simulation did not converge")

    return {
        "codes": codes,
        "total": total,
        "champ": champ_counts / total,
        "final": final_counts / total,
        "sf": sf_counts / total,
        "qf": qf_counts / total,
        "history": history,
    }


# --------------------------------------------------------------- main
def main():
    teams = load_teams()
    strength, fund, w, iters = blended_strength(teams)

    print(f"fundamental fit converged after {iters:,} GD iterations")
    print("feature weights (std. units):",
          [f"{x:+.3f}" for x in w],
          "[logMV, FIFA, culture, logPop, logReg, logGDP, pedigree]")
    print()
    print(f"{'team':<14}{'Elo':>7}{'fund.':>8}{'blend':>8}")
    for c in sorted(strength, key=strength.get, reverse=True):
        print(f"{teams[c]['name']:<14}{teams[c]['elo']:>7.0f}"
              f"{fund[c]:>8.0f}{strength[c]:>8.0f}")

    res = simulate(strength)
    codes = res["codes"]
    total = res["total"]
    print(f"\nMonte Carlo converged after {total:,} tournament simulations")
    print(f"(criterion: max prob change < {CONV_TOL:.4f} over "
          f"{CONV_PATIENCE} consecutive {BATCH:,}-sim batches, "
          f"99% CI half-width < {CI_TOL:.4f})\n")
    order = np.argsort(-res["champ"])
    print(f"{'team':<15}{'win QF? (=R16 win)':>20}{'reach SF':>10}"
          f"{'reach F':>10}{'CHAMPION':>10}")
    for i in order:
        print(f"{teams[codes[i]]['name']:<15}"
              f"{res['qf'][i]:>19.1%} {res['sf'][i]:>9.1%}"
              f"{res['final'][i]:>10.1%}{res['champ'][i]:>10.2%}")

    # write report rows for REPORT.md generation
    with open(os.path.join(HERE, "results.csv"), "w") as f:
        f.write("code,team,reach_qf,reach_sf,reach_final,champion\n")
        for i in order:
            f.write(f"{codes[i]},{teams[codes[i]]['name']},"
                    f"{res['qf'][i]:.4f},{res['sf'][i]:.4f},"
                    f"{res['final'][i]:.4f},{res['champ'][i]:.6f}\n")
    print("\nwrote results.csv")


if __name__ == "__main__":
    main()
