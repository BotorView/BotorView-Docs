# Wavelet analysis

**Analysis → Temporal structure → Wavelet** shows how periodic variability — for example the
annual cycle or multi-year oscillations — changes through time. It computes a continuous
wavelet transform (CWT) with PyWavelets and tests the wavelet power against a red-noise
(AR(1)) or white-noise background, following Torrence & Compo (1998).

The technical reference with every implementation detail is {doc}`../wavelet_analysis`.

## Settings

| Setting | Meaning | Default |
|---|---|---|
| Variable | Numeric column | — |
| Wavelet | Complex Morlet, Complex Gaussian derivative, Morlet, Mexican hat, Gaussian derivative, Shannon, Frequency B-spline (with their parameters) | Complex Morlet $B = 1.5$, $C = 1.0$ |
| Min / Max period | Range of periods in time units | $2\,\Delta t$ / one third of the record |
| Voices / octave | Scales per doubling of the period | 12 |
| Power | Scale-corrected (rectified) or raw $\lvert W\rvert^2$ | Scale-corrected |
| Detrend | Linear or none (the mean is always removed) | Linear |
| Standardize | Scale to unit variance | on |
| Gaps | Stop if gaps exist, Interpolate short gaps, Longest continuous segment | Stop |
| Max gap | Longest interpolated gap (observations) | 3 |
| Background | Red noise (AR(1)) or white noise | Red |
| Monte Carlo series | Surrogates for the global test (0 = no test) | 200 |
| Local test (95 %) | χ² test at every time and period | on |

## Input

The sampling interval $\Delta t$ and the time unit (days, hours, months …) come from the date
index. Missing timestamps on a regular grid are inserted as missing values; irregular data
must be resampled first. At least 32 uninterrupted observations are needed. Missing values
are never dropped silently: by default the analysis stops and reports the gaps.

## Preprocessing

The mean is removed, optionally a least-squares linear trend, and optionally the series is
divided by its standard deviation (power is then relative to the variance). The seasonal
cycle is *not* removed; in daily data the annual cycle usually dominates the spectrum.

## Transform

For the preprocessed series $x_n$, $n = 0,\dots,N-1$, the wavelet coefficient at scale $s$
(in samples) and time $n$ is

$$
W(s, n) = \frac{1}{\sqrt{s}} \sum_{n'=0}^{N-1} x_{n'}\ \psi^{*}\!\left(\frac{n'-n}{s}\right),
$$

computed with `pywt.cwt` (FFT method). For the default complex Morlet wavelet

$$
\psi(t) = \frac{1}{\sqrt{\pi B}}\, e^{-t^2/B}\, e^{\,i 2\pi C t}.
$$

**Scales and periods.** The periods run logarithmically from the minimum to the maximum
period with the chosen number of voices per octave (at most 400 scales). The scale of a
period $P$ (in samples) is $s = f_c\,P$ with the wavelet's centre frequency $f_c$.

**Power.** Raw power is $|W(s,n)|^2$. With PyWavelets' normalisation the raw power of a
sinusoid grows in proportion to the scale, so the default *scale-corrected* (rectified) power (Liu et al., 2007)
divides by it:

$$
\mathcal{P}(s, n) = \frac{|W(s,n)|^2}{s}.
$$

Sinusoids of equal amplitude then have equal power at every period.

**Global wavelet spectrum** — the time average of the power at each period:

$$
\bar{\mathcal P}(s) = \frac1N \sum_{n=0}^{N-1} \mathcal P(s, n).
$$

## Cone of influence

Near the ends of the record the wavelet extends beyond the data and the power is reduced. The
cone of influence (COI) contains the points closer to either end than the e-folding distance
of the wavelet at that scale (the distance at which $|\psi|^2$ falls to $e^{-2}$ of its peak;
for the complex Morlet it is $s\sqrt B$). BotorView measures it numerically for the chosen
wavelet. **Power inside the hatched COI should not be interpreted.**

## Background and significance

**Red-noise background.** The lag-1 autocorrelation of the preprocessed series,

$$
\alpha = \frac{\sum_t x_t\,x_{t+1}}{\sum_t x_t^2}
$$

(limited to $\pm 0.99$), defines an AR(1) process $x_t = \alpha\,x_{t-1} + \varepsilon_t$ with
the normalised spectrum

$$
S(f) \propto \frac{1-\alpha^2}{1 + \alpha^2 - 2\alpha\cos(2\pi f)}
$$

($f$ in cycles per sample; white noise is $\alpha = 0$). The expected background power at each
scale is this spectrum weighted by the squared frequency response of the wavelet filter,
multiplied by the variance of the series (and divided by $s$ for rectified power).

**Local test.** Power at a point is significant at the 95 % level when

$$
\mathcal P(s, n) > \mathcal P_\text{bg}(s)\ \frac{\chi^2_\nu(0.95)}{\nu},
\qquad \nu = 2 \text{ (complex wavelets)},\ \nu = 1 \text{ (real wavelets)}.
$$

The significant regions are outlined on the power map.

**Global test (Monte Carlo).** AR(1) surrogates with the same $\alpha$ and length are
generated (seed 42), preprocessed and transformed like the data; the 95th percentile of their
global spectra is the significance level of the global spectrum.

**Dominant periods** are the local maxima of the global spectrum (the five largest). A peak is
called significant only if it exceeds the Monte Carlo level *and* at least half of its time
points lie outside the COI.

## Interpretation

* About 5 % of the time–period plane exceeds the 95 % level by chance; small isolated
  significant patches are weak evidence. No multiple-testing correction is applied.
* A strong seasonal cycle pushes $\alpha$ close to 1 (for example $\alpha \approx 0.98$ for daily
  temperature). The red-noise background is then very low at short periods, and short-period
  variability easily appears significant; BotorView adds a note when $\alpha > 0.9$.
* Real wavelets (Morlet, Mexican hat, Gaussian derivative) give power that oscillates with the
  phase of the signal; use a complex wavelet to measure amplitude.

## Results

* **Figure** — the analysed series, the power map with significance contours and the COI,
  and the global spectrum with the background and the Monte Carlo level. Period axes are
  logarithmic; above 2,000 time steps the map is averaged in time for display only.
* **Table** — the dominant periods.
* **Exports** — the global spectrum (CSV), the full time × period power grid with
  significance ratio and COI flag (CSV), and the interactive figure (HTML).

## References

Torrence, C. & Compo, G. P. (1998). A practical guide to wavelet analysis. *Bulletin of the
American Meteorological Society*, 79(1), 61–78.

Liu, Y., Liang, X. S. & Weisberg, R. H. (2007). Rectification of the bias in the wavelet power
spectrum. *Journal of Atmospheric and Oceanic Technology*, 24(12), 2093–2102.
