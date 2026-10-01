# The interface

## Navigation

The bar at the top holds the pages in the order of work:

| Page | Shortcut | Purpose |
|---|---|---|
| Home | {kbd}`Ctrl+1` | Overview and quick actions |
| Data | {kbd}`Ctrl+2` | Load and describe a dataset |
| Visualize | {kbd}`Ctrl+3` | Exploratory charts |
| Analysis | {kbd}`Ctrl+4` | Scientific analyses |
| Preprocessing | {kbd}`Ctrl+5` | Prepare data for forecasting |
| Models | {kbd}`Ctrl+6` | Train, evaluate, save and import models |
| Model Comparison | {kbd}`Ctrl+7` | Compare experiments |
| Settings | {kbd}`Ctrl+8` | Preferences |
| Help & About | {kbd}`Ctrl+9` or {kbd}`F1` | Guide, team, citation |

## The context bar

Every page that works on the dataset shows the same bar under its title: the dataset's
name, rows, columns, frequency and period, and a second line with page-specific context
(for example the analysed variable or the model input).

**Change dataset…** loads another file and **Remove** removes the dataset from the
workspace. Both can be undone with **Undo** in the notice that appears under the
navigation bar; undo restores the dataset itself (results computed from it are cleared).

## Steps in the labs

Each model lab shows its workflow as a numbered list of steps. A lab shows only the steps
it implements, but the same kind of step has the same name in every lab and the steps
always appear in this order:

| Step | Meaning |
|---|---|
| Explore | Look at the target series before choosing a model |
| Data | Choose the target and time column and check that the data suit the model |
| Features | Choose and derive the input features |
| Feature Selection | Reduce the features to the most informative ones |
| Split | Split the data chronologically into training, validation and test periods |
| Sequences & Split | Build input windows and split them chronologically |
| Configure | Set the model's parameters |
| Configure & Train | Set the model's parameters and fit it on the training period |
| Harmonics | Preview the Fourier terms that represent the seasonal cycle |
| Train | Fit the model on the training period |
| Validate | Metrics on the validation period, compared with naive and drift baselines |
| Compare Candidates | Compare parameter candidates on the validation period |
| Final Test | Evaluate the chosen configuration once on the held-out test period |
| Evaluate | Metrics on the training, validation and test periods |
| Diagnostics | Residual checks of the fitted model |
| Forecast | Forecast beyond the fitted data |
| Save | Save the model as a `.botor` package that can be imported under Pretrained Models |

Resting the pointer on a step shows its description.

## Parameters

Numeric parameters have a slider next to the number box: drag for a quick change or type an
exact value. Wide ranges (learning rates, numbers of trees …) use a logarithmic slider.

## Appearance

**Settings → General → Appearance** offers the themes *Light*, *Dark* and *Same as the system*,
and five text sizes (90 %, 100 %, 115 %, 130 % and 150 %). A change applies to the running
application immediately — no restart is needed, and the dataset, results and charts on screen
are kept. Re-styling every window takes a few seconds; the pointer shows a busy cursor
meanwhile.
