# Preprocessing

**Preprocessing** ({kbd}`Ctrl+5`) prepares the dataset for forecasting in two steps and hands
the result to the model labs. The data are split in time order; everything that is *learned*
from the data (imputation values, scaling parameters) is learned from the training period
only.

## Step 1: Missing value handling

Choose a method for all columns or for each column individually:

| Method | Missing values are replaced by |
|---|---|
| None | nothing (the values stay missing) |
| Mean | the mean of the column |
| Median | the median of the column (default) |
| Most Frequent | the most frequent value |
| Constant | a value you enter |

The preview and **Download Processed CSV** in this step apply the method to the whole
dataset for inspection. For the models, the imputers are fitted again on the training period
only (step 2).

## Step 2: Preprocessing configuration

* **Target** — the variable to forecast. The target is not scaled.
* **Features** — the input variables.
* **Scaling** — fitted on the training period, applied to all periods (see below).
* **Feature Engineering** — optional derived features (see below).
* **Sequence / Windowing** — input windows for sequence models such as LSTM/GRU.

**Apply Preprocessing** runs the pipeline; **Continue to Models →** opens the model labs with
the result.

## Chronological split

With $N$ rows, the first $\lfloor 0.70N\rfloor$ rows form the training period, the next
$\lfloor 0.15N\rfloor$ rows the validation period and the remaining rows the test period.
Rows are never shuffled, and duplicate timestamps are rejected.

```{mermaid}
flowchart LR
    A[Training 70 %] --> B[Validation 15 %] --> C[Test 15 %]
```

## Scaling

With the statistics of the **training period** ($\mu$, $\sigma$ the population standard
deviation, minimum, maximum, median, interquartile range):

| Scaler | Transformation |
|---|---|
| StandardScaler (default) | $z = (x - \mu_\text{train}) / \sigma_\text{train}$ |
| MinMaxScaler | $z = (x - \min_\text{train}) / (\max_\text{train} - \min_\text{train})$ |
| RobustScaler | $z = (x - \mathrm{median}_\text{train}) / \mathrm{IQR}_\text{train}$ |

Validation and test values can fall outside the training range (for MinMax, outside $[0, 1]$).
A constant feature is only shifted (its scale is set to 1 instead of 0).

## Derived features

**Time features** (need a date index): year, month, day, day of week (0 = Monday), day of year,
quarter, days in month, ISO week, hour and minute.

**Cyclic time features** encode periodic time so that, for example, December and January are
close:

$$
\sin\!\left(\frac{2\pi\,\text{month}}{12}\right),\ \cos\!\left(\frac{2\pi\,\text{month}}{12}\right), \qquad
\sin\!\left(\frac{2\pi\,\text{doy}}{365.25}\right),\ \cos\!\left(\frac{2\pi\,\text{doy}}{365.25}\right),
$$

and likewise for the day of the week (period 7) and the hour (period 24).

**Statistical interactions** — for every pair $(a, b)$ of selected features (never the
target): the product $a \cdot b$ and the ratio $a / b$ (missing where $b = 0$).

**Weather-derived features** — created only when columns with the generic names
`temperature` (and `_max`/`_min`), `humidity`/`rh`, `pressure`/`mslp`,
`rainfall`/`precipitation`, `wind_speed` and `wind_direction` exist. NASA POWER names such as
`T2M` or `PRECTOTCORR` are not recognised.

| Feature | Definition |
|---|---|
| temperature range / midpoint | $T_\max - T_\min$, $(T_\max + T_\min)/2$ |
| pressure / humidity change ($k$ = 1, 3, 6, 12, 24) | $P_t - P_{t-k}$, $RH_t - RH_{t-k}$ |
| wet indicator, intensity | $\mathbf 1[R_t > 0]$, $\max(R_t, 0)$ |
| rainfall accumulation ($w$ = 3, 6, 12, 24, 72) | $\sum_{j=1}^{w} R_{t-j}$ |
| wind components | $u = -S\sin\theta$, $v = -S\cos\theta$; $\sin\theta$, $\cos\theta$ |
| temperature anomaly | $T_t - m_t$ with $m_t$ the mean of the previous 30 values |

Rolling and accumulated features use past values only (shifted by one step).

```{warning}
Features computed from the *current* value of a variable (for example the wet indicator or
the temperature anomaly) contain the target itself when the target is that variable. Do not
select such features for forecasting their own variable.
```

## Sequences (windowing)

For sequence models, each sample is an input window of $L$ time steps (*Sequence length*,
default 30) and the $H$ following target values (*Forecast horizon*, default 1):

$$
X_i = (x_i, \dots, x_{i+L-1}), \qquad y_i = (y_{i+L}, \dots, y_{i+L+H-1}).
$$

The windows contain the features only, and are built separately inside each period, so no
window crosses a period boundary. Each period yields $N_\text{period} - L - H + 1$ samples.

## Missing values after the pipeline

After imputation and scaling, any value that is still missing or infinite in a numeric
column — including the target — is filled within each period by carrying the last valid value
forward, then the next valid value backward, and finally 0. Check the missing values under
**Data** before preprocessing: a target with many gaps is filled in this way.
