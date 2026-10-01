# ARIMA Training Engine

## Overview
The ARIMATrainer implements the `StatisticalModelTrainer` contract for AutoRegressive Integrated Moving Average (ARIMA) models. It is built strictly on the Phase 8S-2 `StatisticalTrainingContract` and leverages `statsmodels.tsa.arima.model.ARIMA` as its mathematical core.

## Configuration
Controlled via `ARIMAConfig`:
- **p**: AutoRegressive (AR) order (must be $\ge 0$).
- **d**: Integrated (I) difference degree (must be $\ge 0$).
- **q**: Moving Average (MA) order (must be $\ge 0$).
- **trend**: Determines deterministic trend ('n' for no trend, 'c' for constant, 't' for linear, etc.).

*Note: Automatic order selection (e.g. `auto_arima`) is currently explicitly **NOT** implemented in this phase. Users must provide manual orders.*

## Data Requirements
ARIMA is a univariate model. The trainer requires:
- Exactly one target variable specified in the spec.
- Target must be fully numeric.
- Target data cannot contain missing values (`NaN`). Missing data must be handled during preprocessing.
- Sufficient observations to satisfy the lag order ($N \ge p + d + q + 1$).

## Splitting and Validation
- **Chronological Split**: Uses `chronological_split` to divide data into Train, Validation, and Test sets without random shuffling.
- **Fitting**: The model is fit *only* on the training dataset. Test data is never used during fitting.
- **Validation Strategy**: A continuous out-of-sample forecast is generated from the end of the training set across both Validation and Test sets. Metrics are evaluated separately against actual values.
- **Future Forecasting**: The trainer supports generating future forecasts through the `forecast(steps)` method, projecting ahead into unseen horizons.

## Confidence Intervals
Statsmodels native prediction intervals are used to generate lower and upper confidence bounds. These are extracted via `get_forecast().conf_int()` and included in the `ForecastResult`.

## Model Statistics and Diagnostics
- **Statistics**: Extracts AIC, BIC, and Log Likelihood where available from the fitted model.
- **Residual Diagnostics**: Evaluates the residuals of the fitted model. Generates ACF arrays (40 lags) and performs a Ljung-Box test for autocorrelation if sufficient lags are present.

## Cancellation & Errors
- The trainer checks for cancellation requests (`TrainingProgress.is_cancelled`) before and after the monolithic statsmodels fit routine.
- Common fitting failures (e.g., non-stationary data that can't be modeled with current orders, linear algebra convergence issues) are trapped and reported gracefully through the `StatisticalTrainingResult` without crashing the application thread.

## Limitations
- Statsmodels' `ARIMA` may sometimes fail to converge on highly irregular data. The exception is captured and exposed via the `errors` property in `StatisticalTrainingResult`.
- If a proper DatetimeIndex with a strict frequency is not provided, the model falls back to integer-based step indexes for forecasts. No dates are fabricated.
