# Stationarity

**Analysis → Temporal structure → Stationarity** tests whether a series has a unit root
(Augmented Dickey–Fuller test), shows its autocorrelation structure (ACF and PACF) and its
first difference. Many statistical forecasting models (for example ARIMA) assume a
stationary series, possibly after differencing.

## Settings

Only the **Variable**. The significance level is 0.05, the ACF/PACF use up to 40 lags, and
the difference is of first order.

Missing values are removed before the test — the observations on either side of a gap are
joined, and the first difference across a gap spans it.

## Augmented Dickey–Fuller (ADF) test

The regression (with a constant) is

$$
\Delta x_t = c + \gamma\,x_{t-1} + \sum_{i=1}^{p} \delta_i\,\Delta x_{t-i} + \varepsilon_t ,
$$

with the hypotheses $H_0\!: \gamma = 0$ (unit root, non-stationary) and
$H_1\!: \gamma < 0$ (stationary). The test statistic is $\hat\gamma / \mathrm{SE}(\hat\gamma)$.

* The number of lagged differences $p$ is chosen by the Akaike information criterion among
  $0,\dots,p_{\max}$ with $p_{\max} = \min\bigl(\lceil 12\,(n/100)^{1/4}\rceil,\ \lfloor n/2\rfloor - 2\bigr)$.
* The p-value and the 1 %, 5 % and 10 % critical values follow MacKinnon's approximations.
* **Decision** — $p \le 0.05$: *likely stationary*; otherwise *likely non-stationary*.

Trends, seasonality and structural breaks affect the result, and a single test summarises the
whole record.

## Autocorrelation function (ACF)

$$
r_k = \frac{c_k}{c_0}, \qquad c_k = \frac1n\sum_{t=1}^{n-k} (x_t-\bar x)(x_{t+k}-\bar x),
$$

for lags $k = 0,\dots,L$ with $L = \min(40, \lfloor n/2\rfloor - 1)$. The 95 % bounds
(Bartlett) are $r_k \pm 1.96\sqrt{v_k}$ with
$v_k = \bigl(1 + 2\sum_{j=1}^{k-1} r_j^2\bigr)/n$.

## Partial autocorrelation function (PACF)

The partial autocorrelation $\phi_{kk}$ is the last coefficient of an autoregression of order
$k$ fitted with the Yule–Walker equations (using the autocovariances $c_k$ above). Its 95 %
bounds are $\pm 1.96/\sqrt n$.

A slowly decaying ACF suggests non-stationarity; for a stationary AR($p$) process the PACF
cuts off after lag $p$, for an MA($q$) process the ACF cuts off after lag $q$.

## Differencing

$$
\nabla x_t = x_t - x_{t-1}
$$

is drawn together with the original series. Differencing removes a stochastic trend. The panel
does not repeat the ADF test on the differenced series; in ARIMA-type models the differencing
is part of the model (the order $d$, see {doc}`../models/statistical`).

## Results

* **Summary** — ADF statistic, p-value and conclusion.
* **Charts** — the ADF table (statistic, p-value, lags, observations, critical values), the
  ACF and PACF, and the original with the differenced series.
* **Export** — a CSV table with the test results and the ACF/PACF values including their
  95 % bounds (`ci_lower`, `ci_upper`), and the chart as HTML.
