# BotorView

**Explore | Analyze | Predict** — a desktop application for weather and climate
time-series analysis, forecasting and visualization.

BotorView takes you from a weather or climate dataset (for example a NASA POWER
daily series for a location) to a documented analysis and a validated forecast:

1. **Load** a CSV file; dates, missing values and the sampling frequency are recognised.
2. **Visualize** distributions, time series, seasonal averages and correlations.
3. **Analyse** trends, seasonality, wavelets, stationarity, change points, anomalies,
   extremes, correlations and weather regimes — every analysis explains its method.
4. **Prepare** the data for forecasting with a strictly chronological, leakage-free workflow.
5. **Model** with statistical, machine-learning and deep-learning methods, each evaluated on
   held-out validation and test periods against simple baselines.
6. **Compare** the experiments and export results, charts and model packages.

```{admonition} Scientific principles
:class: note
Time order is never broken: data are split chronologically into training, validation and
test periods; imputation and scaling are fitted on the training period only; and every
method states its assumptions and how it treats missing values.
```

```{toctree}
:maxdepth: 2
:caption: Getting started

getting-started/installation
getting-started/quickstart
getting-started/interface
```

```{toctree}
:maxdepth: 2
:caption: User guide

user-guide/data
user-guide/visualize
user-guide/analysis
user-guide/preprocessing
user-guide/models
user-guide/model-comparison
user-guide/settings
```

```{toctree}
:maxdepth: 2
:caption: Analysis methods

analysis/trends
analysis/seasonality
analysis/wavelet
analysis/stationarity
analysis/change-points
analysis/anomalies
analysis/extremes
analysis/correlations
analysis/weather-regimes
```

```{toctree}
:maxdepth: 2
:caption: Forecasting models

models/evaluation
models/statistical
models/machine-learning
models/deep-learning
models/pretrained
```

```{toctree}
:maxdepth: 1
:caption: About

about
```

```{toctree}
:maxdepth: 1
:caption: Developer reference

ui_design_system
model_artifact_contract
statistical_training_contract
arima_training
sarima_training
arima_ui_integration
deep_learning
wavelet_analysis
```
