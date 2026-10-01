# Anomalies

**Analysis → Events → Anomalies** flags observations that are statistically unusual
compared with the whole record. An anomaly is a *statistical flag* — it may be an extreme
weather event, a data error or neither, and should be investigated before it is interpreted.

## Settings

| Setting | Choices | Default |
|---|---|---|
| Variable | Any numeric column | — |
| Method | Z-score, IQR | Z-score |
| Threshold (Z-score) | Any number > 0 | 3.0 |
| Multiplier (IQR) | Any number > 0 | 1.5 |

## Methods

Non-numeric and infinite values are treated as missing. The statistics are computed once from
all valid observations of the record ($n$ values).

### Z-score

$$
\bar x = \frac1n\sum_t x_t, \qquad
\sigma = \sqrt{\frac1n\sum_t (x_t-\bar x)^2}, \qquad
z_t = \frac{x_t-\bar x}{\sigma}.
$$

An observation is flagged when $|z_t| > \tau$ (threshold $\tau$, default 3). $\sigma$ is the
population standard deviation. If $\sigma = 0$ only values different from the mean are
flagged, so a constant series has no anomalies.

The z-score suits roughly symmetric variables (for example temperature). For skewed variables
such as precipitation, the IQR method is usually more appropriate.

### IQR (interquartile range)

With the quartiles $Q_1$ and $Q_3$ (linear interpolation between the sorted values) and
$\mathrm{IQR} = Q_3 - Q_1$, an observation is flagged when

$$
x_t < Q_1 - k\,\mathrm{IQR} \quad\text{or}\quad x_t > Q_3 + k\,\mathrm{IQR}
$$

(multiplier $k$, default 1.5). If $\mathrm{IQR} = 0$, values different from the median are
flagged.

### Anomaly rate

$$
\text{anomaly rate} = 100\,\frac{N_\text{flagged}}{N_\text{valid}}\ \%.
$$

## Missing values and time

Missing values stay in the series and are never flagged. The analysis does not remove a
seasonal cycle: in a strongly seasonal variable, the flagged values tend to cluster in the
warmest or coldest part of the year. The time index is used only for the chart's axis
(without dates the axis is the observation order).

## Results

* **Summary** — variable, method, threshold or multiplier, number of anomalies, anomaly
  rate, number of observations and whether dates were used.
* **Chart** — the series with the anomalies marked as open circles.
* **Export** — a CSV table of all observations with the columns `value`, `is_anomaly` and
  `method`, and the chart as an interactive HTML file.
