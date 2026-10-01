# Extremes

**Analysis → Events → Extremes** finds observations beyond a threshold and groups consecutive
exceedances into *events* (for example heat-wave days or heavy-rain spells). Exceedances are
relative to the chosen threshold; they are not automatically hazards or disasters.

## Settings

| Setting | Choices | Default |
|---|---|---|
| Variable | Any numeric column | — |
| Method | Percentile, Absolute | Percentile |
| Percentile | $0 < p < 100$ | 95 |
| Threshold (Absolute) | Any number | 30 |
| Direction | High, Low, Both | High |
| Min Duration | Integer $\ge 1$ (observations) | 1 |
| Gap Tolerance | Integer $\ge 0$ (observations) | 0 |

## Thresholds

Non-numeric, infinite and missing values are removed first; all steps below use the $n$
remaining observations in their time order.

### Percentile

The $p$-th percentile $T_p$ of the record is computed by linear interpolation between the
sorted values $x_{(0)} \le \dots \le x_{(n-1)}$: with $h = (n-1)\,p/100$,

$$
T_p = x_{(\lfloor h\rfloor)} + (h-\lfloor h\rfloor)\,\bigl(x_{(\lfloor h\rfloor+1)} - x_{(\lfloor h\rfloor)}\bigr).
$$

| Direction | Extreme when |
|---|---|
| High | $x_t \ge T_p$ |
| Low | $x_t \le T_{100-p}$ |
| Both | $x_t \le T_{100-p}$ or $x_t \ge T_p$ |

The percentile you enter always describes the *upper* tail: with $p = 95$, **Low** uses the
5th percentile and **Both** uses the 5th and 95th percentiles. For **Both**, choose $p > 50$;
otherwise the two thresholds cross.

The percentile is computed over the whole record, not per season or calendar day.

### Absolute

With a threshold $c$ in the variable's units:

| Direction | Extreme when |
|---|---|
| High | $x_t \ge c$ |
| Low | $x_t \le c$ |
| Both | $x_t \le -c$ or $x_t \ge c$ |

**Both** uses thresholds symmetric about zero, which is meaningful for anomalies or
differences, not for strictly positive variables.

## Events

1. **Gap tolerance $g$** — a run of at most $g$ non-extreme observations between two extreme
   observations is counted as part of the event (gaps before the first or after the last
   extreme are not bridged).
2. **Events** are the maximal runs of consecutive (bridged) extreme observations. The
   duration $D = \text{end} - \text{start} + 1$ counts observations, including bridged ones.
3. Events shorter than **Min Duration** are discarded.

For each event the table gives start, end, duration, peak value (maximum for high extremes,
minimum for low extremes), mean value, and the **magnitude** (cumulative exceedance):

$$
M_\text{high} = \sum_{t\in\text{event}} \max(x_t - T, 0), \qquad
M_\text{low} = \sum_{t\in\text{event}} \max(T - x_t, 0).
$$

With **Both**, both sums are formed and the event is labelled *upper* or *lower* by the
larger one.

Summary statistics: the number of extreme observations (without bridged ones) and their
fraction of $n$, the number of events, and the longest duration and largest magnitude.

## Missing values and time

Because missing values are removed before events are formed, "consecutive" means
consecutive *valid* observations — an event can run across a gap in the record. Durations are
numbers of observations; for daily data they equal days only when the record is complete.

## Results

* **Summary** — threshold (for percentiles also the actual value), direction, number and
  fraction of extreme observations, number of events.
* **Chart** — the series, the threshold line(s), the extreme observations and the events as
  shaded periods (the first 50 events are shaded).
* **Export** — the event table as CSV and the chart as interactive HTML.
