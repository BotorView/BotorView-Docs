# Analysis

**Analysis** ({kbd}`Ctrl+4`) collects the scientific analyses, grouped by the question they
answer. Choose an analysis on the left, then its variable and settings, and run it. Long
analyses (for example the wavelet significance test) run in the background with a progress
bar and **Cancel**, so the application stays responsive.

| Group | Analysis | Question |
|---|---|---|
| Temporal structure | {doc}`../analysis/trends` | Is the variable increasing or decreasing over the record? |
| | {doc}`../analysis/seasonality` | What are the trend, the seasonal cycle and the residual? |
| | {doc}`../analysis/wavelet` | Which periodicities are present, and when? |
| | {doc}`../analysis/stationarity` | Are the mean and variance stable (unit root)? |
| | {doc}`../analysis/change-points` | Where do the mean or the variance change? |
| Events | {doc}`../analysis/anomalies` | Which observations are statistically unusual? |
| | {doc}`../analysis/extremes` | When is a threshold exceeded, and for how long? |
| Relationships | {doc}`../analysis/correlations` | Which variables vary together? |
| | {doc}`../analysis/weather-regimes` | Which typical combinations of variables recur? |

Every analysis panel has:

* a **Method & assumptions** section (collapsed) with the defaults, how missing values are
  treated and the limitations;
* a summary and an interactive chart;
* **exports** — the results as CSV and the chart as an interactive HTML file (the save
  dialog opens in the export directory, see {doc}`settings`).

The analyses never change the dataset. Results are cleared when the dataset changes.
