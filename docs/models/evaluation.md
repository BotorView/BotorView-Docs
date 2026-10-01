# Evaluation and validation

Every model in BotorView is evaluated on data it has not seen: the record is split in time
order into a **training**, a **validation** and a **test** period, the model is fitted on the
training period only, and the forecasts for the later periods are compared with the
observations.

## Chronological split

```{mermaid}
flowchart LR
    A["Training period<br/>(fit)"] --> B["Validation period<br/>(compare, tune)"] --> C["Test period<br/>(final check)"]
```

* The rows are never shuffled, so no future observation is used to fit the model.
* Preprocessing that learns from the data (imputation, scaling) is fitted on the training
  period only (see {doc}`../user-guide/preprocessing`).
* The validation period is used to compare configurations; the test period should be looked
  at once, for the configuration finally chosen (**Final Test** step).

The split proportions depend on the lab: the Preprocessing page uses 70 / 15 / 15 %, the
statistical labs use the Preprocessing split when there is one (otherwise their own
training share, default 80 %, with the rest divided equally), and the machine-learning labs
split the rows remaining after feature engineering (default 70 / 15 / 15 %).

## How forecasts are evaluated

| Model family | Validation and test forecasts |
|---|---|
| Statistical (ARIMA, SARIMA/SARIMAX, DHR, TBATS, VARMAX, ETS) | One multi-step forecast from the end of the training period, without refitting: the validation period covers forecast horizons $1,\dots,n_\text{val}$, the test period horizons $n_\text{val}+1,\dots,n_\text{val}+n_\text{test}$. Exogenous regressors take their observed values. |
| Prophet | Prediction at the validation and test dates from the model fitted on the training period (with observed regressor values). |
| Machine learning | One-step-ahead predictions: each prediction uses the *observed* lagged values of the target. |
| Deep learning | Each input window of observed values predicts the next $H$ target values. |

```{important}
One-step-ahead errors (machine and deep learning) are much smaller than the errors of a
multi-step forecast over the whole validation period (statistical models). Compare models of
different families with this difference in mind.
```

## Metrics

For the $n$ pairs of observation $y_i$ and forecast $\hat y_i$ (pairs with a missing value are
left out) and the errors $e_i = y_i - \hat y_i$:

| Metric | Definition | Notes |
|---|---|---|
| MAE | $\displaystyle \frac1n\sum_i \lvert e_i\rvert$ | in the units of the variable |
| MSE | $\displaystyle \frac1n\sum_i e_i^2$ | squared units |
| RMSE | $\sqrt{\text{MSE}}$ | penalises large errors |
| MAPE | $\displaystyle \frac{100}{n}\sum_i \left\lvert \frac{e_i}{y_i}\right\rvert$ % | undefined when any $\lvert y_i\rvert < 10^{-8}$ (for example zero rainfall) |
| SMAPE | $\displaystyle \frac{100}{n}\sum_i \frac{\lvert e_i\rvert}{(\lvert y_i\rvert + \lvert \hat y_i\rvert)/2}$ % | between 0 and 200 % |
| $R^2$ | $\displaystyle 1 - \frac{\sum_i e_i^2}{\sum_i (y_i - \bar y)^2}$ | 1 is perfect; negative is worse than the mean |
| Mean error (bias) | $\displaystyle \frac1n\sum_i e_i$ | positive: forecasts too low on average |

The machine-learning labs also report the median, maximum and minimum absolute error, the
explained variance $1 - \operatorname{Var}(e)/\operatorname{Var}(y)$ and the standard
deviation of the errors, and warn about possible overfitting when the validation RMSE is more
than 1.5 or 2 times the training RMSE, when $R^2$ drops by more than 0.3 from training to
validation, or when the test RMSE is more than 1.5 times the validation RMSE.

## Baselines

A model is useful only if it beats simple forecasts. The statistical labs show two baselines
on the validation period, forecast from the end of the training period ($T$ observations):

$$
\text{Naive:}\quad \hat y_{T+h} = y_T, \qquad
\text{Drift:}\quad \hat y_{T+h} = y_T + h\,\frac{y_T - y_1}{T-1}, \qquad h = 1,\dots,n_\text{val}.
$$

## Residual diagnostics

For statistical models the **Diagnostics** step checks the residuals $\hat\varepsilon_t$ of the
fitted model (training period): their mean, standard deviation, autocorrelation (40 lags) and
the Ljung–Box test

$$
Q = n(n+2)\sum_{k=1}^{h} \frac{r_k^2}{n-k}, \qquad h = \min(10, n-1),
$$

where $r_k$ is the residual autocorrelation at lag $k$. Under the hypothesis of uncorrelated
residuals, $Q$ follows approximately a $\chi^2$ distribution; a small p-value means the model
has left structure in the residuals. The information criteria

$$
\text{AIC} = -2\ln L + 2k, \qquad \text{AICc} = \text{AIC} + \frac{2k(k+1)}{n-k-1}, \qquad
\text{BIC} = -2\ln L + k\ln n
$$

($L$ the maximised likelihood, $k$ the number of parameters) compare models fitted to the same
data; lower is better.
