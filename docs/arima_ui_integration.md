# ARIMA UI Integration

This document outlines the architecture and behavior of the `StatisticalModelingPage` connection to the production `ARIMATrainer`.

## UI -> Training Service Flow
The `StatisticalModelingPage` relies on a `QThread` and `QObject` (`TrainerWorker`) pattern to prevent the PySide6 UI from blocking during long-running ARIMA estimation.

When a user clicks **Train Model**:
1. `_validate_before_train()` performs lightweight assertions (dataset existence, target existence, and observation bounds).
2. The UI values (p, d, q, target, train split, forecast horizon) are mapped into the `StatisticalTrainingSpec` and `ARIMAConfig`.
3. `_set_busy_state(True)` disables input controls and displays a `QProgressBar`.
4. A `TrainerWorker` instance is initialized with the spec and dataset, and pushed to a new `QThread`.
5. Inside the thread, the `ARIMATrainer` handles chronological splitting, statsmodels fitting, test set evaluation, and result generation.
6. The `TrainerWorker` emits `progress` signals tied to the `worker_progress.report()` bridge, which updates the UI status label and progress bar.
7. Upon successful generation of a `StatisticalTrainingResult`, the thread emits `finished`, tearing down the `QThread` and triggering `_on_training_finished()`.

## Result Invalidation
Any modification to the data or model parameters must invalidate the currently visible result to prevent staleness:
- Dataset swap
- Target variable modification
- p, d, q, or forecast horizon change
- Train/Validation/Test slider modification

These signals are bound to `_invalidate_results()` which clears the results placeholder and disables the "Save Model" button.

## Result Display
Once a valid `StatisticalTrainingResult` is returned, the Results Card is populated:
- **Metrics**: Formatted HTML label displaying MAE, MSE, RMSE, R², Mean Error, AIC, BIC, Log Likelihood, and Ljung-Box statistics.
- **Forecast Chart**: `pyqtgraph.PlotWidget` visualizing the observed chronological target series appended with the out-of-sample Forecast mean. Upper and lower confidence bounds are shaded blue.
- **Forecast Table**: A `QTableWidget` listing the individual indexed observations for the forecast and its 95% confidence intervals.

## Train vs Save vs Register vs Activate
The application distinctly segregates these responsibilities:
- **Train Model**: Computes the parameters and provides evaluation feedback. Exists ephemerally in session memory.
- **Save Model**: Not yet implemented (will save the `joblib`/metadata bundle to disk).
- **Import/Register/Activate**: Governed entirely by the existing `ModelManager` architecture.

## Known Limitations
- Automatic Order Selection (`auto_arima`) is currently unsupported and disabled in the UI.
