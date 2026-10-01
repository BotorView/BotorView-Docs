# Change points

**Analysis → Temporal structure → Change Points** screens a series for positions where the
mean or the variance changes, by comparing a window before and a window after every
position. A change point is a statistical signal — it may reflect a climate shift, a station
relocation, an instrument change or a data problem, and is not automatically a weather or
climate event.

## Settings

| Setting | Meaning | Default |
|---|---|---|
| Method | Mean Shift, Variance Shift, Mean and Variance Shift | Mean Shift |
| Window $w$ | Observations on each side (integer $\ge 2$) | 12 |
| Threshold | Minimum score of a change point ($> 0$) | 3.0 |
| Min Distance | Minimum number of observations between two change points ($\ge 1$) | 12 |
| Min Segment | Minimum observations on each side ($\ge 2$) | 12 |

```{important}
* The **variance score lies between 0 and 1**. For *Variance Shift*, set the threshold below 1
  (for example 0.5); with the default 3.0 no variance change can be detected, and *Mean and
  Variance Shift* then reports mean shifts only.
* Keep **Min Segment ≤ Window**: each side always contains $w$ observations, so a larger
  Min Segment excludes every position.
```

## Method

Non-numeric, infinite and missing values are removed; windows count valid observations.
For every candidate position $\tau$ with at least $m = \max(w, \text{Min Segment})$ values
on each side, the windows are

$$
L = (x_{\tau-w},\dots,x_{\tau-1}), \qquad R = (x_{\tau+1},\dots,x_{\tau+w})
$$

(the value at $\tau$ belongs to neither). With the window means $\bar x_L, \bar x_R$ and sample
variances $s_L^2, s_R^2$:

**Mean shift** — the pooled two-sample $t$ statistic:

$$
Z_\tau = \frac{|\bar x_R - \bar x_L|}{\sqrt{s_p^2\,(1/w + 1/w)}}, \qquad
s_p^2 = \frac{(w-1)\,s_L^2 + (w-1)\,s_R^2}{2w-2}.
$$

**Variance shift** — the relative difference of the variances:

$$
V_\tau = \frac{|s_R^2 - s_L^2|}{s_R^2 + s_L^2} \in [0, 1].
$$

**Mean and variance shift** — $\max(Z_\tau, V_\tau)$.

**Selection** — positions with a score $\ge$ Threshold are taken in order of decreasing score;
a position is accepted when it is at least *Min Distance* observations from every position
already accepted.

## Interpretation

The score is a screening statistic, not a formal test: there is no p-value and no correction
for testing many positions. In daily data the seasonal cycle alone produces many mean shifts
— remove the seasonal cycle (for example with {doc}`seasonality`) or use anomalies before
screening for climate shifts.

## Results

* **Summary** — method, number of change points, observations.
* **Chart** — the series with the change points marked (and labelled when there are at most
  20).
* **Export** — a CSV table with every observation, its score and whether it is a change
  point, and the chart as HTML.
