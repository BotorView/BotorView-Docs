# Quick start

This walk-through takes about ten minutes with a daily NASA POWER CSV file (any CSV with a
date column and numeric variables works the same way).

## 1. Load the data

Open **Data** (or press {kbd}`Ctrl+2`) and choose **Browse Files**. The Data page shows:

* the detected time index, period and sampling frequency (for example *D (daily)*);
* the columns, the number of missing values and a preview of the first rows;
* notes on anything changed while reading the file (for example a NASA POWER header block
  that was skipped or fill values such as −999 that were treated as missing).

The dataset now appears in the context bar at the top of every page, with
**Change dataset…** and **Remove** (both can be undone).

## 2. Visualize

**Visualize** gives a first look: distributions, box plots, time series, monthly averages,
a correlation heat map and the pattern of missing values.

## 3. Analyse

**Analysis** groups the analyses by the question they answer:

* **Temporal structure** — Trends, Seasonality, Wavelet, Stationarity, Change Points;
* **Events** — Anomalies, Extremes;
* **Relationships** — Correlations, Weather Regimes.

Choose an analysis, a variable and the settings, then run it. Each analysis has a
**Method & assumptions** section and exports its results (CSV) and chart (HTML).

## 4. Prepare the data for forecasting

**Preprocessing** handles missing values, selects the target and features, scales the data
and, for deep learning, builds input windows. The data are split chronologically into
training, validation and test periods; imputers and scalers are fitted on the training
period only. **Continue to Models** hands the result to the model labs.

## 5. Train and evaluate models

**Models** has a lab for every model family (Statistical, Machine Learning, Deep Learning)
and **Pretrained Models** for importing saved models. Every lab lists its steps on the left
(Configure, Train, Evaluate, Diagnostics, Forecast, Save …). Models are fitted on the
training period and evaluated on the later validation and test periods, next to naive and
drift baselines.

```{tip}
Deep-learning training can take a long time. BotorView asks for confirmation before it
starts; importing a pretrained model is often the faster first step.
```

## 6. Compare and save

**Model Comparison** lists every completed experiment with its metrics and exports the
comparison. A lab's **Save** step writes a `.botor` model package that can be imported
again under **Models → Pretrained Models**.
