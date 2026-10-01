# Wavelet Analysis

Wavelet Analysis shows how periodic variability changes through time. It
computes a continuous wavelet transform of one variable and tests the wavelet
power against a red-noise (AR(1)) or white-noise background.

In the application it is under **Analysis → Temporal structure → Wavelet**.

This document describes what the implementation does, the assumptions it
makes, and how its results should (and should not) be interpreted. Keep it in
step with the code.

## 1. Code layout

| File | Role |
|---|---|
| `botorview/core/analysis/wavelet.py` | All computation. `WaveletConfig`, `analyze_wavelet()` and `WaveletResult`, with no Qt dependency. |
| `botorview/visualization/wavelet.py` | `plot_wavelet(result)`: the Plotly figure. |
| `botorview/io/analysis_export.py` | `wavelet_global_spectrum_frame()` and `wavelet_power_frame()`: the CSV tables. |
| `botorview/ui/wavelet_panel.py` | `WaveletPanel`: the controls, the results, and the background run. |
| `botorview/ui/workers/analysis_worker.py` | `AnalysisWorker` / `start_worker`: the thread pattern (see `ui_design_system.md` §8). |
| `botorview/ui/analysis_notes.py` | The in-app "Method & assumptions" text. |

**Dependency.** PyWavelets (`pywt`), declared in `pyproject.toml` as
`PyWavelets>=1.6,<2`. The development environment has PyWavelets 1.9.0.

The 1.9.0 wheel ships a generated `pywt/version.py` that still says `1.8.0`,
so `pywt.__version__` prints `1.8.0` while pip, conda and
`importlib.metadata` report `1.9.0`. The application reads the version from
`importlib.metadata`.

## 2. Input and sampling interval

The analysis takes one numeric column of the workspace DataFrame. It never
modifies the input DataFrame.

**With a `DatetimeIndex`**, the timestamps must be unique and increasing.

* If pandas can infer a frequency, it sets the sampling interval and the
  time unit of all periods:

  | Inferred frequency | Time unit |
  |---|---|
  | Daily (`D`) | days |
  | Hourly (`h`) | hours |
  | Minutes | minutes |
  | Seconds | seconds |
  | Weekly | weeks |
  | Business days | business days |
  | Monthly (`MS`/`ME`) | months |
  | Quarterly | months (step 3) |
  | Yearly | years |

  Multiples keep the unit, so 6-hourly data gives `dt = 6` hours.
* If no frequency can be inferred (usually because timestamps are missing), the
  data must lie on a regular grid:
  * **Calendar-month data.** If every timestamp is a month start, or every one
    a month end, at midnight, the step is the greatest common divisor of the
    month differences: 1 is monthly, 3 quarterly (any anchor month), 12
    yearly.
  * **Otherwise, a fixed step.** The most common time step is used, and every
    step must be a whole multiple of it.

  The missing timestamps are inserted as missing values and then go through
  gap handling (§3), so they are never dropped silently.
* Irregular spacing is rejected with an explanation. Resample the data first.
  Frequencies without a supported time unit, such as semi-monthly or
  sub-second, are also rejected.

**Without a `DatetimeIndex`**, rows are analysed in their order. `dt = 1`
and periods are in *observations*.

**Assumption.** Every step is treated as the same length. Calendar months and
business days therefore count as equal steps, even though real months differ
in length and weekends are skipped.

## 3. Missing values and gaps

1. Missing values at the start and end of the series are trimmed, and the
   number trimmed is reported.
2. Missing values inside the record (including inserted timestamps) are
   handled by `gap_handling`:

   | Option | Behaviour |
   |---|---|
   | `reject` (default, "Stop if gaps exist") | Error. It gives the number of missing values and gaps, and the length and position of the longest gap. |
   | `interpolate` ("Interpolate short gaps") | Linear interpolation, allowed only if **every** gap is at most `max_interpolated_gap` consecutive values long (default 3, UI range 1–10). If any gap is longer, the analysis stops with an error: nothing is partly filled. The number of interpolated values is reported. |
   | `longest_segment` ("Longest continuous segment") | Analyses the longest uninterrupted run. Its start, end and the number of excluded observations are reported. |

3. At least 32 uninterrupted observations are required.

Everything done in steps 1–2 is recorded in `WaveletResult.gap_report` and
listed in the result notes.

Linear interpolation smooths the filled values, which slightly lowers power
at the shortest periods near the gaps.

## 4. Preprocessing

* The mean is always removed.
* `detrend="linear"` (default) removes a least-squares linear trend
  (`scipy.signal.detrend`).
* `standardize=True` (default) scales the series to unit variance (population
  standard deviation). Power is then in units of the series variance.
* A series that is constant after preprocessing is rejected. This includes a
  purely linear series when detrending is on.

No deseasonalisation is done in this version. In daily climate data the annual
cycle usually dominates the spectrum, and it raises the lag-1 autocorrelation
(see §7). Remove the seasonal cycle before running the analysis if variability
other than the annual cycle is the question.

## 5. Transform

**Wavelets.** Each family is exposed with its PyWavelets parameters:

| Family | PyWavelets name | Parameters (range) | Type |
|---|---|---|---|
| Complex Morlet (default) | `cmorB-C` | B bandwidth (0.1–10, default 1.5), C centre frequency (0.1–5, default 1.0) | complex |
| Complex Gaussian derivative | `cgauN` | order N (1–8, default 2) | complex |
| Morlet | `morl` | none | real |
| Mexican hat | `mexh` | none | real |
| Gaussian derivative | `gausN` | order N (1–8, default 2) | real |
| Shannon | `shanB-C` | B, C as above | complex |
| Frequency B-spline | `fbspM-B-C` | spline order M (1–10, default 2), B, C | complex |

The default `cmor1.5-1.0` has |ψ(t)|² ∝ exp(−2t²/1.5). It is close in shape to
the Morlet wavelet used by Torrence & Compo (1998), which corresponds to B = 2.
The complex Morlet is recommended for power spectra.

Caveats shown in the UI:

* Real-valued wavelets give power that oscillates with the phase of the
  signal.
* Shannon and frequency B-spline wavelets are poorly localised in time, which
  widens the cone of influence.

**Scales.**

* Periods run from `min_period` (default 2·dt, the shortest resolvable period)
  to `max_period` (default one third of the record length). They are spaced
  logarithmically with `voices_per_octave` scales per doubling (default 12,
  UI range 4–32).
* At most 400 scales are allowed.
* The scale for a period P (in samples) is `s = f_c · P`, where
  `f_c = pywt.central_frequency(wavelet)`. The reported period is `1 / f`,
  using the frequencies returned by `pywt.cwt`.
* For wavelets with a broad spectrum (Mexican hat, low-order Gaussian
  derivatives), the peak of the response is less sharply defined, so this
  period mapping is less precise.

**Transform.** `pywt.cwt(x, scales, wavelet, sampling_period=dt, method="fft")`.

**Power.**

* PyWavelets normalises its wavelets so that the raw power |W|² of a sinusoid
  grows in proportion to the scale.
* The default `power_normalization="rectified"` therefore divides the power by
  the scale (the rectification of Liu et al., 2007). Sinusoids of equal
  amplitude then give equal power at every period; the tests check this for
  periods 16 and 128.
* `raw` keeps |W|².

**Global wavelet spectrum.** The time average of the power at each period, over
all time points. The share of time points outside the cone of influence is
reported for each period (`coi_free_fraction`).

## 6. Cone of influence (COI)

The COI is measured numerically for the selected wavelet and parameters, using
the e-folding definition of Torrence & Compo (1998):

1. For each scale, a unit impulse is transformed with the same `pywt.cwt` call.
   This gives the effective filter.
2. The e-folding distance is the largest distance from the filter peak at which
   |filter|² is still at least e⁻² of its peak.
3. The distances are made non-decreasing across scales, to remove
   discretisation ripple.

A point is inside the COI when its distance to the nearer end of the record is
less than the e-folding distance for its scale. Power inside the COI is reduced
by edge effects and should not be interpreted.

For `cmorB-C` the analytical e-folding distance is s·√B. The tests check that
the numerical value agrees within a few percent (the median ratio is 1.00).

## 7. Background and significance

**Background model.**

* `background="red"` (default): an AR(1) process with lag-1 autocorrelation α,
  estimated from the preprocessed series as
  α = Σ x_t·x_{t+1} / Σ x_t².
  α is limited to ±0.99, with a note.
* `background="white"`: α = 0.

**Expected background power.** The expected wavelet power of a stationary
AR(1) process with the series' variance is computed for PyWavelets' actual
filters:

* It is the discrete AR(1) spectrum (normalised to unit variance), integrated
  against the squared frequency response of each scale's effective filter
  (§6), and multiplied by the series variance.
* With rectified power, it is divided by the scale as well.
* This is the expectation for an infinitely long stationary process, so it
  does not model edge effects. The tests check that the mean power outside the
  COI of simulated white and AR(1) (α = 0.7) noise matches it: the median ratio
  is 1.00 ± 0.05.

**Local test** (`local_significance=True`). Power at a (time, period) point is
significant at level p (95 %) when it exceeds

    expected_power × χ²_ν(p) / ν,     ν = 2 for complex, ν = 1 for real wavelets

This follows Torrence & Compo (1998). It assumes Gaussian noise and, for
complex wavelets, real and imaginary parts that are independent with equal
variance, which holds approximately for analytic wavelets. For simulated
noise, about 5 % of points outside the COI exceed the level (tests: 3.5–7 %;
measured 4.7–5.4 %).

**Global test** (Monte Carlo, `monte_carlo_iterations`).

* The configuration default is 200; the UI allows 0–2000, and 0 skips the test.
* The procedure:
  1. Generate AR(1) surrogates with the same α and length (Gaussian
     innovations, 256-step burn-in, random seed `random_seed`, default 42).
  2. Preprocess each surrogate exactly like the data. When the data is not
     standardised, each surrogate is rescaled to the data's standard deviation.
  3. Transform each surrogate at the same scales.
  4. At each period, the threshold is the p-th percentile of the surrogates'
     global spectra.
* The same seed gives identical thresholds. At least 20 iterations are
  required when the test is on, and more iterations give a more stable
  percentile.
* The uncertainty of the estimated α is not propagated.

**Dominant periods.**

* Local maxima of the global spectrum; the five largest are listed.
* A peak is marked *significant* only if it exceeds the Monte Carlo threshold
  **and** at least half of its time points lie outside the COI.
* Without the Monte Carlo test, peaks are listed as "Not tested".

## 8. Interpreting the results

* **Pointwise tests.** Roughly 5 % of the time–period plane exceeds the 95 %
  level by chance. Across many periods, a few global peaks can too. Small
  isolated significant patches, and peaks only slightly above the level, are
  weak evidence. No multiple-testing correction is applied.
* **High lag-1 autocorrelation.** A strong seasonal cycle pushes α towards 1
  (for example α ≈ 0.98 for daily temperature). The red-noise background is
  then very low at short periods, and short-period variability easily appears
  "significant". The analysis adds a note when α > 0.9.
* **Edges.** Ignore power inside the hatched COI. Long periods have large COIs,
  and a peak near the maximum period is mostly edge-affected (see
  `coi_free_fraction`).
* **Real wavelets.** Their power has ripples at twice the signal frequency.
  Use a complex wavelet to measure amplitude.
* **Standardised power** is relative to the variance of the (detrended)
  series, so it is not comparable in absolute units between variables.

## 9. Outputs and export

`WaveletResult` holds:

* the analysed and original series;
* the periods, scales and power matrix [period × time];
* the global spectrum;
* the COI: e-folding distance, the boundary period at each time, and the
  COI-free fraction;
* α, the expected background, the local and global thresholds and the degrees
  of freedom;
* the dominant periods, the gap report, the preprocessing summary, the notes
  and the configuration.

Exports:

* **Export CSV** (global spectrum): one row per period, with period, unit,
  scale, global power, expected background, the local and global thresholds,
  the COI-free fraction and the global significance flag. The flag is empty
  when the test was not run.
* **Export Power Grid CSV**: one row per (time, period), with power, the local
  significance ratio (power / threshold; > 1 is significant) and an
  inside-COI flag. It asks for confirmation above 500,000 rows.
* **Export HTML**: the interactive figure, which works offline.

**Figure.**

* Panels: the analysed series; the power map, with the local-significance
  contour (ratio = 1) and the hatched COI; and the global spectrum, with the
  background and the Monte Carlo level.
* The period axes are logarithmic, with long periods at the bottom.
* Above 2,000 time steps the power map is averaged over blocks of time steps
  **for display only**. The figure notes this, and the exports keep full
  resolution.

## 10. Performance

The transform itself is fast: about 0.15 s for about 9,000 daily values on
the development machine. Most of the time goes to the Monte Carlo test, at
about 0.1 s per surrogate for the same length, so 200 surrogates take about
20–25 s. The panel runs the analysis in a worker thread with progress and
Cancel, so the interface stays responsive.

## 11. Verification

* `tests/test_wavelet_analysis.py` checks:
  * recovery of known periods in days, months, hours and observations;
  * scale spacing and equal rectified power for equal amplitudes;
  * the COI against s·√B;
  * the background ratio and ≈5 % false positives for white and AR(1) noise;
  * ν for real wavelets and Monte Carlo reproducibility;
  * each gap policy, missing and irregular timestamps;
  * input validation, cancellation and progress, and that the input is not
    mutated;
  * the export frames.
* `tests/test_wavelet_visualization.py` checks the figure traces, the axes,
  the case without significance, and display-only block averaging.
* `tests/test_wavelet_panel.py` checks:
  * the controls, the dynamic wavelet parameters and the configuration they
    produce;
  * error, cancellation and visualization-failure messages;
  * enabling of the exports;
  * a background run, cancelling it, and replacing the dataset during a run;
  * the worker signals and the Analysis-page integration.

## References

Torrence, C. & Compo, G. P. (1998). A practical guide to wavelet analysis.
*Bulletin of the American Meteorological Society*, 79(1), 61–78.

Liu, Y., Liang, X. S. & Weisberg, R. H. (2007). Rectification of the bias in
the wavelet power spectrum. *Journal of Atmospheric and Oceanic Technology*,
24(12), 2093–2102.
