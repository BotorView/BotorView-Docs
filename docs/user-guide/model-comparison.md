# Model comparison

**Model Comparison** ({kbd}`Ctrl+7`) lists every model run completed in the current session,
newest first:

| Column | Content |
|---|---|
| ID, Date | Experiment identifier and time |
| Family, Model, Target | What was trained |
| Features | Number of input features |
| Train/Val/Test | Sizes of the three periods |
| MAE, MSE, RMSE, MAPE, R² | Metrics on the **validation** period (see {doc}`../models/evaluation`) |
| Comparability | *Yes* when the run used the same target and period sizes as most runs |

Select a row to see its configuration. **Refresh Comparison** updates the table and
**Export to CSV** saves it.

Compare runs only when they are comparable (same target and periods), and keep in mind that
the statistical models are evaluated by one multi-step forecast over the validation period,
the machine- and deep-learning models by one-step-ahead predictions.

The list is kept in memory: it is empty when BotorView starts again. Save the models you want
to keep (**Save** step) and export the table.
