# Visualize

**Visualize** ({kbd}`Ctrl+3`) gives a first visual overview of the loaded dataset. Choose a
**Variable** and a **Visualization**, then **Generate Visualization** (the quick buttons draw
a distribution, box plot or time series directly). The charts are interactive: zoom with the
mouse, hover for values, and use the toolbar to reset or save a picture.

| Visualization | What is drawn | Missing values |
|---|---|---|
| Distribution | Histogram of the variable (at most 30 bins; the bin width is chosen automatically). | Left out |
| Box Plot | Median, quartiles $Q_1$, $Q_3$ and whiskers reaching the most extreme values within $1.5\,\mathrm{IQR}$ of the box; values beyond the whiskers are drawn as points. | Left out |
| Time Series | The values against the time index (or the first date column), without resampling. | Gaps in the line |
| Monthly Averages | Calendar-month climatology (see below). | Skipped |
| Correlation Heatmap | Pearson correlation of all numeric columns (see {doc}`../analysis/correlations`). | Pairwise |
| Missing Values | Number of missing values per column (only columns with missing values), labelled with the percentage of rows. | — |

**Correlation Heatmap** and **Missing Values** use all columns and ignore the Variable
selection. **Time Series** and **Monthly Averages** need dates; without them the chart area
says that no date information was found.

## Monthly averages

For each calendar month $m = 1,\dots,12$ the chart shows the mean of all observations that
fall in that month, pooled over all years:

$$
\bar x_m = \frac{1}{|\{t : \mathrm{month}(t) = m\}|}\sum_{t:\ \mathrm{month}(t)=m} x_t .
$$

This is the mean of the observations, not the mean of monthly means, so years with more
observations in a month weigh more. A month without data is left empty.

```{note}
Visualize is for orientation. The analyses under **Analysis** add the statistics, the
method notes and the exports.
```
