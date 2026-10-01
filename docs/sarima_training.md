# SARIMA Training Engine

## Overview

The `SARIMATrainer` is the second statistical model implemented in the BotorView Statistical Modeling Workspace. It extends the `StatsmodelsTrainerMixin` and `StatisticalModelTrainer` base classes, establishing a shared statistical training contract identical to `ARIMATrainer`.

## Configuration Parameters

SARIMA introduces seasonal differencing and seasonal autoregressive/moving average terms, requiring a `SARIMAConfig`:
- **p, d, q**: Non-seasonal autoregressive, differencing, and moving average orders.
- **P, D, Q**: Seasonal autoregressive, differencing, and moving average orders.
- **seasonal_period (m)**: Number of observations per seasonal cycle. (e.g., 12 for monthly data with annual seasonality).
- **trend**: One of "n", "c", "t", "ct". Cannot be "c" or "ct" if `d > 0` or `D > 0` due to integration mapping to polynomial trends.

## Data Constraints

The trainer strictly validates dataset length prior to passing into statsmodels. The minimum required observations to accurately perform seasonal differencing is:
`required_observations = d + (D * seasonal_period) + p + q + P + Q + 1`

## Statsmodels Integration

The engine leverages `statsmodels.tsa.arima.model.ARIMA`, passing the seasonal components natively via `seasonal_order`. It extracts `AIC`, `BIC`, and log-likelihood directly from the fitted object, alongside the Ljung-Box Q-statistic via `acorr_ljungbox`.

All model evaluations (validation/test splits) and diagnostics generation are fully encapsulated within `_statsmodels_utils.py` for direct re-use between both ARIMA and SARIMA trainers.
