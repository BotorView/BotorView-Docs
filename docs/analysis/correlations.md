# Correlations

**Analysis → Relationships → Correlations** computes the correlation matrix of the selected
variables. Correlation indicates statistical association, not causation: weather variables
that share a seasonal cycle or a trend can be strongly correlated without a direct physical
link.

## Settings

| Setting | Choices | Default |
|---|---|---|
| Variables | Two or more numeric columns | All numeric columns |
| Method | Pearson, Spearman | Pearson |
| Missing-data handling | Pairwise, Listwise | Pairwise |

## Methods

### Pearson correlation

For the valid pairs $(x_i, y_i)$, $i = 1,\dots,N$:

$$
r_{xy} = \frac{\sum_i (x_i-\bar x)(y_i-\bar y)}
              {\sqrt{\sum_i (x_i-\bar x)^2\,\sum_i (y_i-\bar y)^2}} .
$$

Pearson's $r$ measures *linear* association and is sensitive to outliers.

### Spearman rank correlation

$\rho$ is the Pearson correlation of the ranks of $x$ and $y$ (tied values get their average
rank). It measures *monotonic* association and is robust to outliers and skewed
distributions such as precipitation.

## Missing values

* **Pairwise** — each coefficient uses all rows where *both* variables are present, so
  different cells can rest on different numbers of observations. The number of valid pairs
  $N_{xy}$ is shown when hovering over a cell.
* **Listwise** — rows with a missing value in *any* selected variable are removed first;
  all coefficients use the same rows.

A coefficient is undefined (blank) when a variable is constant or has too few valid pairs.

## What is not computed

The analysis reports coefficients only — no p-values, no confidence intervals and no lagged
correlations. Weather data are autocorrelated, so the effective number of independent
observations is much smaller than $N$; ordinary significance tests would overstate the
evidence.

## Results

* **Heatmap** — coefficients on a fixed scale from −1 to +1 (two decimals).
* **Export** — a CSV table with one row per variable pair: `variable_1`, `variable_2`,
  `coefficient`, `valid_observations`, `method`, `missing_handling`; and the chart as HTML.
