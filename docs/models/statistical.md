# Statistical models

**Models → Statistical** contains the classical time-series models. Choose the model and the
target; every lab then shows its steps (see {doc}`../getting-started/interface`). All labs use
the evaluation described in {doc}`evaluation`. $B$ denotes the backshift operator,
$B\,y_t = y_{t-1}$, and $\varepsilon_t$ white noise.

| Model | Library | Target | Regressors |
|---|---|---|---|
| ARIMA | statsmodels | one series | — |
| SARIMA / SARIMAX | statsmodels | one series | SARIMAX: exogenous variables |
| Prophet | Prophet | one series | optional |
| Dynamic Harmonic Regression (DHR) | statsmodels | one series | optional |
| TBATS | tbats | one series | — |
| VARMAX | statsmodels | several series jointly | optional |
| Exponential Smoothing State Space (ETS) | statsmodels | one series | — |

## Data preparation

For ARIMA, SARIMA/SARIMAX, Prophet and DHR, remaining missing values in the numeric columns
are filled before the split (last value carried forward, then the next value backward, then
0). TBATS, VARMAX and ETS do not fill anything: a target (or regressor) with missing values in
the modelled period stops the run with an explanation — handle the gaps under
**Preprocessing** first.

## ARIMA

ARIMA($p, d, q$) models the $d$-times differenced series as an ARMA process:

$$
\phi(B)\,(1-B)^d\,\eta_t = \theta(B)\,\varepsilon_t, \qquad y_t = \mu_t + \eta_t,
$$

with $\phi(B) = 1 - \phi_1 B - \dots - \phi_p B^p$, $\theta(B) = 1 + \theta_1 B + \dots + \theta_q B^q$
and the deterministic term $\mu_t$: none (`n`), a constant (`c`), a linear trend (`t`) or both
(`ct`). The parameters are estimated by maximum likelihood (state-space form, Kalman filter).

* **Explore** — the series, its stationarity and autocorrelation, to choose $d$, $p$ and $q$.
* **Compare Candidates** — fits every combination $p = 0,\dots,p_\max$, $q = 0,\dots,q_\max$
  (with the chosen $d$ and trend) on the training period and ranks them by **validation MAE**
  (AIC, BIC, RMSE and $R^2$ are shown for information). Double-click a row to use it.
* **Final Test**, **Diagnostics**, **Forecast** and **Save** follow.

Defaults: $p = 1$, $d = 0$, $q = 1$, no deterministic term.

## SARIMA and SARIMAX

The seasonal model SARIMA($p,d,q$)($P,D,Q$)$_s$ adds seasonal polynomials in $B^s$:

$$
\phi(B)\,\Phi(B^s)\,(1-B)^d(1-B^s)^D\,\eta_t = \theta(B)\,\Theta(B^s)\,\varepsilon_t .
$$

**SARIMAX** is a regression with SARIMA errors, $y_t = \beta^\top x_t + \eta_t$, where $x_t$
are the exogenous variables at time $t$. Their observed values are used for the validation and
test periods; beyond the end of the data the last observed values are repeated.

Defaults: $(1,1,1)(1,1,1)_{12}$, no deterministic term, stationarity and invertibility not
enforced, at most 50 optimiser iterations. At least $d + Ds + p + q + P + Q + 1$ observations
are required. **Compare Candidates** works as for ARIMA, over $p$ and $q$ with the other orders
fixed (defaults $p_\max = 3$, $q_\max = 1$). For daily data with an annual cycle, $s = 365$
makes the model very large —
consider DHR or TBATS instead.

## Prophet

Prophet (Taylor & Letham, 2018) fits an additive regression model

$$
y(t) = g(t) + s(t) + \sum_j \beta_j\,x_j(t) + \varepsilon_t,
$$

with a piecewise-linear trend $g(t)$ whose slope may change at up to 25 changepoints in the
first 80 % of the training period, and seasonalities as Fourier series

$$
s(t) = \sum_{n=1}^{N}\left[a_n\cos\!\left(\frac{2\pi n t}{P}\right) + b_n\sin\!\left(\frac{2\pi n t}{P}\right)\right]
$$

for yearly, weekly and daily periods $P$ (chosen automatically by default). Defaults:
seasonality prior scale 10, changepoint prior scale 0.05, additive seasonality.

## Dynamic Harmonic Regression (DHR)

DHR represents a long seasonal cycle of period $m$ by $K$ Fourier pairs and models the rest
with ARIMA errors:

$$
y_t = \beta^\top x_t + \sum_{k=1}^{K}\left[\alpha_k \sin\!\left(\frac{2\pi k t}{m}\right)
      + \gamma_k \cos\!\left(\frac{2\pi k t}{m}\right)\right] + \eta_t, \qquad
\eta_t \sim \text{ARIMA}(p, d, q).
$$

$K \le m/2$. The time index $t$ continues from the training period into the validation and
test periods, so the harmonics stay in phase. The **Harmonics** step previews the Fourier
terms. If the default optimiser fails, the fit is retried with the Nelder–Mead and then the
BFGS method. Defaults: $p = 1$, $d = 0$, $q = 1$, $m = 12$.

## TBATS

TBATS (De Livera, Hyndman & Snyder, 2011) — **T**rigonometric seasonality, **B**ox–Cox
transformation, **A**RMA errors, **T**rend and **S**easonal components — handles several
seasonal cycles and non-integer periods such as 365.25 days. With the Box–Cox transformed
series $y_t^{(\omega)}$:

$$
\begin{aligned}
y_t^{(\omega)} &= \ell_{t-1} + \phi\, b_{t-1} + \sum_{i=1}^{T} s_{t-1}^{(i)} + d_t, \\
\ell_t &= \ell_{t-1} + \phi\, b_{t-1} + \alpha\, d_t, \\
b_t &= (1-\phi)\, b + \phi\, b_{t-1} + \beta\, d_t, \\
s_t^{(i)} &= \sum_{j=1}^{k_i} s_{j,t}^{(i)}, \qquad \lambda_j^{(i)} = \frac{2\pi j}{m_i},\\
s_{j,t}^{(i)} &= s_{j,t-1}^{(i)}\cos\lambda_j^{(i)} + s_{j,t-1}^{*(i)}\sin\lambda_j^{(i)} + \gamma_1^{(i)} d_t, \\
s_{j,t}^{*(i)} &= -s_{j,t-1}^{(i)}\sin\lambda_j^{(i)} + s_{j,t-1}^{*(i)}\cos\lambda_j^{(i)} + \gamma_2^{(i)} d_t,
\end{aligned}
$$

where $\ell_t$ is the level, $b_t$ the trend (damped by $\phi$), $m_i$ the seasonal periods,
$k_i$ the number of harmonics of period $m_i$, and $d_t$ an ARMA process of the errors.

| Setting | Meaning | Default |
|---|---|---|
| Seasonal periods | Observations per cycle, separated by commas | by frequency: daily `7, 365.25`, weekly `52.18`, monthly `12`, quarterly `4`, hourly `24, 168` |
| Box-Cox transformation | Automatic, Yes, No (needs positive values) | Automatic |
| Trend, Damped trend | Automatic, Yes, No | Automatic |
| Consider ARMA errors | ARMA model for $d_t$ | on |

Components on *Automatic* are included or excluded by the AIC of the fitted candidates; the
number of harmonics per period is also chosen by AIC. At least two cycles of the longest
period are required. When the data contain values $\le 0$, the Box–Cox transformation is
switched off. Because TBATS fits several candidate models, it is slow for long daily series.

## VARMAX

VARMAX models $k$ series $\mathbf y_t$ (the target and the other *endogenous* series) jointly:

$$
\mathbf y_t = \boldsymbol\nu_t + \sum_{i=1}^{p} A_i\,\mathbf y_{t-i} + B\,\mathbf x_t
            + \boldsymbol\varepsilon_t + \sum_{j=1}^{q} M_j\,\boldsymbol\varepsilon_{t-j},
\qquad \boldsymbol\varepsilon_t \sim N(\mathbf 0, \Sigma),
$$

with the deterministic terms $\boldsymbol\nu_t$ (constant, linear trend, both or none), the
coefficient matrices $A_i$, $M_j$ and $B$, and exogenous regressors $\mathbf x_t$. The model
is estimated by maximum likelihood; each series can respond to the past of every other series.

| Setting | Meaning | Default |
|---|---|---|
| AR order $p$, MA order $q$ | $p > 0$ or $q > 0$ | 1, 0 |
| Deterministic terms | Constant, None, Linear time trend, Constant and linear trend | Constant |
| Enforce stationarity and invertibility | Restrict the parameters | on |
| Endogenous | At least one series besides the target | — |
| Exogenous regressors | Not endogenous | none |

The number of parameters grows with $k^2(p+q)$; the lab checks that the training period is
long enough. With $q > 0$ the parameters of a VARMA model may not be uniquely identified, and
statsmodels warns about it. Beyond the end of the data, exogenous regressors repeat their last
observed values (the forecast step says so).

## Exponential Smoothing State Space (ETS)

ETS(Error, Trend, Seasonal) models (Hyndman et al., 2008) are exponential smoothing methods in
innovations state-space form, fitted by maximum likelihood (statsmodels `ETSModel`). Each
component is **N**one, **A**dditive or **M**ultiplicative; a trend can be **d**amped. For
example, ETS(A, Ad, A):

$$
\begin{aligned}
y_t &= \ell_{t-1} + \phi\,b_{t-1} + s_{t-m} + \varepsilon_t, \\
\ell_t &= \ell_{t-1} + \phi\,b_{t-1} + \alpha\,\varepsilon_t, \\
b_t &= \phi\,b_{t-1} + \beta\,\varepsilon_t, \\
s_t &= s_{t-m} + \gamma\,\varepsilon_t,
\end{aligned}
$$

and with multiplicative error $y_t = \mu_t\,(1 + \varepsilon_t)$, where $\mu_t$ is the one-step
forecast. The lab shows the model in this notation as you configure it.

| Setting | Choices | Default |
|---|---|---|
| Error | Additive, Multiplicative | Additive |
| Trend | None, Additive, Multiplicative (+ damped) | None |
| Seasonal | None, Additive, Multiplicative | None |
| Seasonal period $m$ | Integer $\ge 2$ | by frequency: daily 7, weekly 52, monthly 12, quarterly 4, hourly 24 |

Multiplicative components require strictly positive data; a seasonal model needs at least two
seasonal cycles, and at least 10 observations are needed. Prediction intervals are exact for
linear (additive) models and simulated otherwise.

## Forecast step

* **TBATS, VARMAX, ETS** — the chosen configuration is fitted again on the whole series
  (training, validation and test periods), and the forecast starts after the last observation.
  The evaluation metrics remain those of the training-period fit.
* **ARIMA, SARIMA/SARIMAX, DHR, Prophet** — the forecast continues the model fitted on the
  training period.

Prediction intervals are 95 % intervals, except Prophet's, which are Prophet's default 80 %
uncertainty intervals.

## Saving

**Save** writes a `.botor` package with the model fitted on the training period and its
metadata (see {doc}`pretrained` and the {doc}`../model_artifact_contract`).

## References

De Livera, A. M., Hyndman, R. J. & Snyder, R. D. (2011). Forecasting time series with complex
seasonal patterns using exponential smoothing. *Journal of the American Statistical
Association*, 106(496), 1513–1527.

Hyndman, R. J., Koehler, A. B., Ord, J. K. & Snyder, R. D. (2008). *Forecasting with
Exponential Smoothing: The State Space Approach*. Springer.

Taylor, S. J. & Letham, B. (2018). Forecasting at scale. *The American Statistician*, 72(1),
37–45.

Box, G. E. P., Jenkins, G. M., Reinsel, G. C. & Ljung, G. M. (2015). *Time Series Analysis:
Forecasting and Control* (5th ed.). Wiley.
