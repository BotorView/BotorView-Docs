# Machine-learning models

**Models → Machine Learning** trains gradient-boosted decision trees — **XGBoost**,
**LightGBM** and **CatBoost** — on features derived from the past of the target. The steps
are Data, Features, Feature Selection, Split, Configure, Train, Evaluate, Diagnostics,
Forecast and Save.

## Features

Tree models do not know about time; the time structure is given to them as features. All
features at time $t$ use values *before* $t$ only, except the regressors and the calendar.

| Feature | Definition | Default |
|---|---|---|
| Target lags | $y_{t-k}$ | $k = 1, 2, 3, 7, 14$ |
| Rolling statistics | mean and standard deviation of $y_{t-w},\dots,y_{t-1}$ | $w = 7, 14, 30$ |
| Exponentially weighted mean | EWM of $y_{t-1}, y_{t-2},\dots$ with span 7 and 14 | off |
| Calendar | month, day of week, day of year, quarter | on |
| Regressors | other numeric columns at time $t$ (Feature Selection step) | none |

Rows with a missing target or feature are removed after the features are built (at least 5
rows must remain); the first rows are always removed because their lags do not exist yet.

## Split and training

The remaining rows are split chronologically (default 70 % training, 15 % validation, rest
test). The models minimise the squared error of the one-step prediction on the training
period. **Early stopping** (default 50 rounds; 0 disables it) stops adding trees when the
validation error has not improved for that many rounds.

A gradient-boosted ensemble predicts

$$
\hat y = \sum_{m=1}^{M} \eta\, f_m(\mathbf x),
$$

where each $f_m$ is a regression tree fitted to the gradient of the loss of the previous
ensemble and $\eta$ is the learning rate. The libraries differ in how trees are grown
(XGBoost: depth-wise; LightGBM: leaf-wise; CatBoost: symmetric trees with ordered boosting).

| Model | Parameters in the lab (defaults) |
|---|---|
| XGBoost | n_estimators 500, learning_rate 0.05, max_depth 6, subsample 0.8, colsample_bytree 0.8, reg_alpha 0, reg_lambda 1 |
| LightGBM | n_estimators 500, learning_rate 0.05, num_leaves 31, max_depth −1 (no limit), subsample 0.8, feature_fraction 0.8, reg_alpha 0, reg_lambda 0 |
| CatBoost | iterations 500, learning_rate 0.05, depth 6, l2_leaf_reg 3, bootstrap type |

The random seed (default 42) makes the results reproducible.

## Evaluation

The training, validation and test metrics (see {doc}`evaluation`) are **one-step-ahead**:
every prediction uses the observed lags. The Evaluate step also shows the feature importance
and warns about possible overfitting; Diagnostics shows the residuals on the test period.

## Forecast

The Forecast step forecasts $h$ steps (default 30) beyond the last observation
**recursively**: for each step the features of the next timestamp are computed from the
history, the target is predicted, and the prediction is added to the history for the lags
and rolling statistics of the following steps. Errors therefore accumulate with the horizon.
Future values of the regressors are not known; they keep their last observed values.
Without target lags or rolling features, all steps are predicted from the same inputs apart
from the calendar features.

Choose the frequency of the forecast timestamps (D, W, MS, H) or *auto* to take it from the
dates.
