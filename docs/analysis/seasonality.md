# Seasonality (decomposition)

**Analysis → Temporal structure → Seasonality** separates a series into trend, seasonal and
residual components with the classical moving-average decomposition
(`statsmodels.tsa.seasonal.seasonal_decompose`).

## Settings

| Setting | Choices | Default |
|---|---|---|
| Variable | Any numeric column | — |
| Model | Additive, Multiplicative | Additive |
| Seasonal Period $P$ | Positive integer (observations), optional | blank |

For the **annual cycle of daily data use $P = 365$**. When the period is blank, it is taken
from the data frequency — for daily data this is a *weekly* period of 7, which is rarely the
cycle of interest in climate data.

## Models

$$
\text{Additive:}\quad x_t = T_t + S_t + R_t, \qquad
\text{Multiplicative:}\quad x_t = T_t \cdot S_t \cdot R_t .
$$

Use the additive model when the seasonal swing has a constant size, the multiplicative model
when it grows with the level (all values must then be positive).

## Method

1. **Trend** — a centred moving average over one period. For odd $P = 2k+1$:

   $$
   T_t = \frac1P \sum_{j=-k}^{k} x_{t+j};
   $$

   for even $P = 2k$ the two end values get half weight:

   $$
   T_t = \frac1P\left[\tfrac12 x_{t-k} + \sum_{j=-k+1}^{k-1} x_{t+j} + \tfrac12 x_{t+k}\right].
   $$

   The trend is undefined for the first and last $\lfloor P/2\rfloor$ observations.

2. **Seasonal component** — the detrended series $D_t = x_t - T_t$ (multiplicative:
   $x_t / T_t$) is averaged for each position $i$ in the cycle, and the averages are centred:

   $$
   \bar s_i = \operatorname{mean}\{D_t : t \equiv i \pmod P\}, \qquad
   s_i = \bar s_i - \frac1P\sum_{j} \bar s_j \quad\Bigl(\text{multiplicative: } s_i = \bar s_i \Big/ \tfrac1P\textstyle\sum_j \bar s_j\Bigr),
   $$

   and $S_t = s_{t \bmod P}$ repeats the same pattern in every cycle.

3. **Residual** — $R_t = x_t - T_t - S_t$ (multiplicative: $R_t = x_t / (T_t S_t)$).

The cycle positions are counted from the first observation, not from a calendar date; with
$P = 365$ on daily data, leap days shift the phase slightly over many years.

## Requirements

* The series must be **contiguous**: missing values at the start and end are trimmed, but
  missing values inside the record stop the analysis with an explanation. Fill or shorten the
  record first (for example under **Preprocessing**).
* At least two full periods ($n \ge 2P$) are needed.
* Without a date index, the period must be entered.

## Limitations

* The seasonal pattern is assumed identical in every cycle; changes in the seasonal cycle end
  up in the residual.
* Trend and residual are missing for half a period at each end.

## Results

* **Chart** — four panels: observed, trend, seasonal and residual.
* **Export** — a CSV table with the four components per time step and the chart as HTML.
