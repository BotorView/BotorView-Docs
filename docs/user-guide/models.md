# Models

**Models** ({kbd}`Ctrl+6`) holds one lab per model family:

| Family | Models | Details |
|---|---|---|
| Statistical | ARIMA, SARIMA/SARIMAX, Prophet, Dynamic Harmonic Regression, TBATS, VARMAX, Exponential Smoothing State Space (ETS) | {doc}`../models/statistical` |
| Machine Learning | XGBoost, LightGBM, CatBoost | {doc}`../models/machine-learning` |
| Deep Learning | LSTM, GRU, BiLSTM | {doc}`../models/deep-learning` |
| Pretrained Models | Import, inspect and activate saved models | {doc}`../models/pretrained` |

A model whose library is not installed stays in the list, disabled, with the reason and the
installation command.

## Working in a lab

1. **Choose the model and the target** (and regressors where the model supports them).
2. Follow the **steps** on the left — Configure, Train, Evaluate, Diagnostics, Forecast,
   Save … (the step names are explained in {doc}`../getting-started/interface`).
3. Training runs in the background with progress and **Cancel**.
4. Every model is fitted on the training period and evaluated on the later validation and
   test periods ({doc}`../models/evaluation`); completed runs appear in
   {doc}`model-comparison`.
5. **Save** writes a `.botor` package.

The labs use the result of **Preprocessing** when there is one; otherwise they work on the
loaded dataset directly.
