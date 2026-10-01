# Weather regimes

**Analysis → Relationships → Weather Regimes** groups observations (for example days) into
$k$ recurring combinations of the selected variables with K-means clustering. A regime is a
statistical cluster — it describes typical combinations such as "hot and dry" or "cool and
humid", but it is not by itself a physical weather type.

## Settings

| Setting | Choices | Default |
|---|---|---|
| Variables | One or more numeric columns | none selected |
| Number of Regimes $k$ | Integer $\ge 2$ | 3 |
| Scale Data | Yes, No | Yes |
| Random State | Integer | 42 |

## Method

1. **Rows with a missing value** in any selected variable are excluded; they receive no
   regime.
2. **Standardisation** (when *Scale Data* is on): each variable is transformed to
   $z_{ij} = (x_{ij}-\bar x_j)/s_j$ with its mean $\bar x_j$ and population standard deviation
   $s_j$. Without scaling, variables with large numeric ranges dominate the distances.
3. **K-means** partitions the observations into $k$ clusters $C_1,\dots,C_k$ with centroids
   $\mu_r$ by minimising the within-cluster sum of squares

   $$
   W = \sum_{r=1}^{k}\ \sum_{i\in C_r} \lVert z_i - \mu_r \rVert^2 .
   $$

   The algorithm (scikit-learn, Lloyd iterations) starts 10 times from k-means++
   initialisations and keeps the best solution; *Random State* makes the result reproducible.
   Each observation is assigned to its nearest centroid.

The number of regimes is chosen by you — BotorView does not select $k$ automatically. The
regime numbers are arbitrary labels.

## Statistics

* **Size** of regime $r$: $n_r$ observations, $100\,n_r/n$ % of the clustered observations.
* **Profile**: the mean of every variable in the regime, in the original units.
* **Transitions**: the number of times regime $a$ is directly followed by a different regime
  $b$, counted between consecutive clustered observations:

  $$
  T_{ab} = \#\{t : L_t = a,\ L_{t+1} = b,\ a \ne b\}.
  $$

## Time order

K-means ignores the time order: two observations with the same values fall into the same
regime whatever their dates. Time enters only in the timeline chart and in the transition
counts. Because excluded rows are skipped, a transition can join observations on either side
of a gap.

## Results

* **Summary** — variables, $k$, scaling and the size of every regime.
* **Charts** — regime timeline, regime profiles (means), regime sizes and, when there are any,
  the transition counts.
* **Export** — a CSV table with the regime of every clustered observation, and the chart as
  HTML.

```{note}
K-means favours compact clusters of similar size. Try several values of $k$ and check that
the regimes are physically interpretable before using them.
```
