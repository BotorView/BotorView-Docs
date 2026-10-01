# Trends

**Analysis → Temporal structure → Trends** estimates the long-term direction of a variable
with a parametric test (linear regression) and two non-parametric methods (Mann–Kendall and
Sen's slope).

## Settings

| Setting | Choices | Default |
|---|---|---|
| Variable | Any numeric column | — |
| Analysis Depth | Comprehensive Analysis (All), Linear Regression, Mann-Kendall Test, Sen's Slope | All |

The significance level is fixed at $\alpha = 0.05$; at least 3 valid observations are needed.

## Data preparation and time axis

Non-numeric, infinite and missing values are removed. The remaining $n$ values $y_1,\dots,y_n$
are analysed **in observation order**, with $x_i = i-1 = 0,1,\dots,n-1$. The dates are used
only for the chart. Consequently:

* **slopes are per valid observation** — for complete daily data this is per day
  (multiply by 365.25 for a slope per year); with gaps in the record it is not a slope per
  unit of time;
* gaps in the record are closed up, not filled.

## Linear regression (ordinary least squares)

The line $\hat y_i = a + b\,x_i$ minimises $\sum_i (y_i - \hat y_i)^2$:

$$
b = \frac{\sum_i (x_i-\bar x)(y_i-\bar y)}{\sum_i (x_i-\bar x)^2}, \qquad a = \bar y - b\,\bar x .
$$

The correlation coefficient $r$ gives $R^2 = r^2$, the share of variance explained by the
line. The standard error of the slope and the test of $H_0\!: b = 0$ are

$$
\mathrm{SE}_b = \sqrt{\frac{\sum_i (y_i-\hat y_i)^2/(n-2)}{\sum_i (x_i-\bar x)^2}}, \qquad
t = \frac{b}{\mathrm{SE}_b} = r\sqrt{\frac{n-2}{1-r^2}},
$$

with a two-sided p-value from Student's $t$ distribution with $n-2$ degrees of freedom.
The trend is called significant when $p < 0.05$.

## Mann–Kendall test

The Mann–Kendall statistic counts how often later values exceed earlier ones:

$$
S = \sum_{i<j} \operatorname{sgn}(y_j - y_i).
$$

BotorView computes it as Kendall's rank correlation $\tau_b$ between time and value
(`scipy.stats.kendalltau`):

$$
\tau_b = \frac{S}{\sqrt{N_0\,(N_0 - n_1)}}, \qquad N_0 = \frac{n(n-1)}{2},\quad
n_1 = \sum_k \frac{u_k(u_k-1)}{2},
$$

where $u_k$ are the sizes of groups of tied values. For small series without ties the
p-value is exact; otherwise it comes from the normal approximation

$$
z = \frac{S}{\sqrt{\operatorname{Var} S}}, \qquad
\operatorname{Var} S = \frac{n(n-1)(2n+5) - \sum_k u_k(u_k-1)(2u_k+5)}{18}, \qquad
p = 2\,[1-\Phi(|z|)] .
$$

The test detects monotonic (not necessarily linear) trends and does not assume normally
distributed data.

## Sen's slope

Sen's (Theil–Sen) slope is the median of all pairwise slopes:

$$
\beta = \operatorname*{median}_{i<j} \frac{y_j - y_i}{x_j - x_i}, \qquad
\text{intercept} = \operatorname{median}(y) - \beta\,\operatorname{median}(x).
$$

It is robust to outliers. The 95 % confidence interval of $\beta$ (Sen, 1968) takes the
order statistics of the $N = n(n-1)/2$ pairwise slopes at ranks
$(N \mp 1.96\sqrt{\operatorname{Var} S})/2$. Sen's slope has no significance flag of its own;
use the Mann–Kendall p-value.

## Summary with "All"

* **Overall direction** — majority vote of the directions (signs) of the three methods;
  a tie gives "no trend".
* **Statistically significant** — *Yes* when linear regression **or** Mann–Kendall is
  significant.

The direction shown is the sign of the estimate; read it together with the significance
line. A constant series gives slope 0, $p = 1$ and "no trend".

## Limitations

* Daily weather data are autocorrelated, and neither test corrects for autocorrelation or
  seasonality — p-values for daily series tend to be too optimistic.
* A significant trend describes the record analysed; it does not identify a cause.

## Results

* **Summary** and **Test statistics** (all numbers of every method run).
* **Chart** — the observations and, when linear regression was run, the fitted line.
* **Export** — one CSV row per method (with `slope_units = per valid observation`) and the
  chart as HTML.
