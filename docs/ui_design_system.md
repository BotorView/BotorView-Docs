# BotorView UI Design System

This document describes how the desktop interface is styled and how charts are
rendered. It covers the design tokens, the application theme, the shared UI
components, the Plotly template and the model-availability presentation.

## 1. Design tokens — `botorview/design_tokens.py`

All colours, typography, spacing and radii live in one framework-free module.
Both the Qt theme and the Plotly template import it; nothing else should
hard-code colour values.

**Brand colours.** The palette is derived from the BotorView logo:

| Token | Value | In the logo |
|---|---|---|
| `BRAND_NAVY` | `#00163E` | Outline of the "BotorView" lettering |
| `BRAND_BLUE` | `#0098F8` | The globe |
| `BRAND_CYAN` | `#00D8F8` | The "V", "EXPLORE" |
| `BRAND_GREEN` | `#70F030` | The leaf, "ANALYZE" |
| `BRAND_YELLOW` | `#F8E000` | "PREDICT", the sun |
| `BRAND_ORANGE` | `#F8A800` | The sun's rays |

The bright logo colours are not readable as lines on white, so charts use
deeper shades (`CHART_BLUE` `#0B6BCB`, `CHART_ORANGE` `#F08C00`,
`CHART_GREEN` `#2E9A3E`, `CHART_CYAN` `#0AA5E9`, `CHART_NAVY` `#0B1F3F`).

**Two palettes.** `LIGHT_PALETTE` and `DARK_PALETTE` define the same token
names; `use_palette("light" | "dark")` copies one into the module globals
(`APPEARANCE` names the active one). Main tokens:

| Token | Light | Dark | Use |
|---|---|---|---|
| `BACKGROUND` | `#F4F7FB` | `#0D1522` | Application canvas |
| `SURFACE` | `#FFFFFF` | `#142033` | Panels, cards, group boxes, plot paper and plot area |
| `TEXT` | `#0E1C33` | `#E7EEF7` | Primary text |
| `ACCENT` | `#0A66C2` | `#1D74D0` | Primary buttons, active navigation, focus, slider fill |
| `VIZ_PRIMARY` | `#0B6BCB` | `#3D9BF0` | Primary data series |
| `WORDMARK` / `WORDMARK_X` | `#00163E` / `#0088C0` | `#F2F6FB` / `#00D8F8` | The application name in the logo's treatment |

Blue is the interactive accent; cyan, green and yellow appear in the brand
stripe under the navigation bar and in the Analysis groups, and the chart
colours in plots and in the success / warning states, so the interface is not
overly colourful. The main foreground /
background pairs of both palettes have a WCAG contrast of at least 4.5:1
(`tests/test_preferences_and_branding.py`).

These tokens are derived from the palette above:

* **Secondary text** (`TEXT_SECONDARY`, `TEXT_TERTIARY`), checked for contrast on the background.
* **Semantic status colours**: `INFO`, `SUCCESS`, `WARNING`, `ERROR`, each with a background and a border shade.
* **Visualization palettes**: an ordered categorical palette, a sequential scale and a diverging scale.

**Typography.** Fonts are resolved at runtime from a preference list:

* Sans: Inter → IBM Plex Sans → … → DejaVu Sans.
* Mono: JetBrains Mono → … → DejaVu Sans Mono.

No font files are bundled. When the display cut of the UI family is installed
(e.g. "Inter Display" alongside "Inter"), page titles use it.

**Type scale.** Every text element uses one of six sizes, chosen by what the
element *is*, so the same kind of heading or text has the same size on every
page. The sizes below are the default (100 %) text size; Settings → General
scales all of them (`use_text_scale`, 90–150 %):

| Style | Size | Weight | Used for |
|---|---|---|---|
| Page title | 28 px | semibold | One per page, at the top ("Analysis Workspace", "Welcome to BotorView") |
| Panel title | 22 px | semibold | The main working area inside a page: an analysis panel, a model lab, a preprocessing step, System Information |
| Section title | 18 px | semibold | Cards, group boxes, result blocks and chart captions ("Select Model", "Model Summary") |
| Base | 17 px | regular | Body text, labels, inputs, buttons, tabs, navigation and table cells; also subsection titles (semibold) |
| Small | 15 px | regular | Captions, notes, table headers, tooltips |
| Caption | 14 px | semibold, uppercase | Group labels (overlines), statistic labels, chart tick labels |

Statistic values use the panel-title size and the wordmark the app-title size
(20 px, heavy). Charts follow the same scale (`visualization/theme.py`).

**Line height.** Descriptive paragraphs and result summaries — Help & About,
"Method & assumptions", model descriptions, the Analysis overview and the
analysis result summaries — use a relaxed line height of 145 %
(`LINE_HEIGHT_RELAXED`). Qt style sheets cannot set line height, so it is
applied in rich text: `rich_text.relaxed()` and the `RelaxedLabel` component.

The application font uses light (vertical) hinting. Tables and lists use
tabular figures, so numbers line up in columns.

Results written as HTML (model summaries, diagnostics) pass through
`botorview/ui/rich_text.py: style_headings()`. Qt draws `<h2>`/`<h3>` at up to
twice the body size and ignores a `font-size` on them, so the function turns
`<h1>`–`<h3>` into section titles and `<h4>`–`<h6>` into subsection titles.

**Geometry.** Spacing follows a 4 / 8 / 12 / 16 / 24 / 32 px scale. Border radii are 4–6 px
(`RADIUS_SM`, `RADIUS_MD`). Pages use 28 px horizontal and 20 px vertical margins
(`PAGE_MARGIN_H/V`); the navigation bar is 65 px high (`TOP_BAR_HEIGHT`, which
grows with larger text sizes).

**Window.** The main window opens as a 16:10 rectangle that fills the
available screen **height** (96 % of it, leaving room for the title bar) and
is not stretched to the width (`WINDOW_ASPECT`, `WINDOW_SCREEN_FILL`,
`botorview/ui/window_geometry.py`). Only screens narrower than 16:10 limit
the width, keeping the ratio. The minimum size is limited to the screen on
smaller displays.

Some desktops maximize any new window that covers most of the screen (GNOME's
"auto-maximize", on by default in Ubuntu), which would stretch the window to the
full width. During the first four seconds after start-up (`AUTO_MAXIMIZE_WATCH_MS`), `MainWindow` treats a
maximize it did not request as that automatic maximize: the maximized size
gives the usable screen area (the desktop's panels excluded, which Qt cannot
see on Wayland), and the window returns to a normal window that is 16:10 and as
tall as that area (`fit_to_height`) — 1532 × 958 on a 1920 × 1080 Ubuntu screen
with the top bar and dock. Maximizing later is left alone. The measured area is
remembered per screen size (`usable_screen_area` in the settings file), so
later starts open at that size directly: the window keeps a fixed size for
the first 1.5 s (`HOLD_SIZE_MS`), which stops the automatic maximize, and becomes resizable
afterwards. "Restore Default Settings" forgets the measurement. On Wayland the
desktop, not the application, decides where a window is placed; GNOME centres
new windows only when "Center New Windows" is enabled (GNOME Tweaks → Windows). With Settings → General → "Reopen at the
last window size and position", the window instead restores the geometry
saved when it was last closed.

## 2. Application theme — `botorview/ui/theme.py`

`apply_theme(app)` is called in `botorview.app.run_app()`, and again with
`force=True` when the theme or text size changes (§11). It:

1. selects the Fusion style;
2. installs a Qt palette built from the active (light or dark) tokens;
3. sets the application font;
4. installs **one** application-wide stylesheet;
5. makes the Plotly template the default for new figures.

Widgets do **not** call `setStyleSheet`. Instead they declare what they are
through dynamic properties, which the application stylesheet matches:

| Helper | Property | Examples |
|---|---|---|
| `set_role(w, …)` | `role` | Labels: `page-title`, `panel-title`, `section-title`, `subsection-title`, `muted`, `caption`, `note`, `overline`, `field-label`, `kv-key`/`kv-value`, `summary`, `mono`, `code-block`, `step-number`.<br>Frames: `panel`, `controls`, `banner-info`/`-success`/`-warning`, `danger-zone`, `separator`, `nav-separator`, `dropzone`.<br>Text areas: `log`.<br>Lists: `subnav`. |
| `set_variant(b, …)` | `variant` | `primary`, `danger`, `ghost`, `action`, `topnav`, `subnav`, `disclosure` (default = secondary) |
| `set_tone(l, …)` | `tone` | Status text colour: `success`, `warning`, `error`, `info`, `muted` (`None` resets) |

The helpers re-polish the widget, so a property may be changed after
construction (e.g. a status label switching from *info* to *success*).

Why properties instead of type selectors: a rule such as `QFrame { border: … }`
also matches every `QLabel` inside the frame, because `QLabel` is a `QFrame`.
Property selectors (`QFrame[role="panel"]`) match only the widget that declares
the role.

Two further conventions:

* **Indicators and arrows.** Checkbox/radio indicators and combo/spin-box arrows
  are small SVGs generated from the tokens into a per-user temporary directory
  (`theme_asset_dir()`). Fusion stops drawing these sub-controls once they are
  styled.
* **Mnemonics.** Qt treats `&` in tab, group-box and button captions as a keyboard
  mnemonic. Captions that should show an ampersand must use `&&`.

## 3. Shared components — `botorview/ui/components/`

| Component | Purpose |
|---|---|
| `PageHeader(title, subtitle)` | Standard page header. It is a `QVBoxLayout` (added as the first item of a page layout) exposing `title_label`/`subtitle_label`. |
| `Panel(title=None, variant="panel"\|"controls")` | Thin-bordered rectangular section; add content to `.body`. `CardFrame` is the titled variant used by the modeling pages (keeps the historical `.layout` attribute). |
| `InlineMessage(text, severity)` | Word-wrapped info/success/warning/error message; `show_message()` / `clear_message()`. |
| `EmptyState(title, message, action_text)` | Empty/prerequisite state with an optional primary action. |
| `KeyValueGrid(rows)` | Metadata presentation; values are selectable. |
| `ExportBar`, `save_dataframe_csv`, `save_figure_html` | Shared export controls and dialogs. They default to the configured export directory. HTML exports embed plotly.js so they open offline anywhere. |
| `PlotView` | Offline Plotly rendering (see §4). |
| `WorkspaceContextBar` | The dataset/workspace context strip (see §8). |
| `CollapsibleSection(title, content)` | Disclosure section used for "Method & assumptions". The title's `&` is escaped automatically. |
| `StepTabWidget` | A lab's workflow as a numbered vertical step list next to the current step's page. Offers the `QTabWidget` methods the labs use (`addTab`, `count`, `tabText`, `setCurrentIndex`, `currentChanged` …). |
| `ChronologicalSplitView` | Model-input facts and a proportional training / validation / test bar with counts, shares and dates. `planned_split_parts` computes the periods with `chronological_split`, the function the trainers use. |
| `MetricsTable` | The one metrics layout: rows of model · period, then Observations, MAE, RMSE, MSE, MAPE (%), R² and Bias, in fixed order and format. Trainer key spellings (`mae`, `MAE`, `Mean Error` …) are normalised. |
| `ResponsiveColumns(stretches, breakpoint=1100, min_widths=None)` | Side-by-side columns (`.columns`, a list of `QVBoxLayout`) that stack vertically when the available width — the visible width of the enclosing scroll area — is below the breakpoint or below what the columns need side by side (their minimum widths, or the declared `min_widths` for content whose need is hidden by an inner scroll area). The switch is deferred to the next event-loop pass, because changing a layout's direction while Qt applies its geometry is unsafe. Used by Help & About and by the three model-family pages (model cards beside the lab, `LAB_MIN_WIDTH = 900`), so no page scrolls sideways. |
| `RelaxedLabel(text)` | Word-wrapped label shown with the relaxed line height. |
| `UndoBar` | Slim notice with an action under the navigation bar ("“weather.csv” was removed. Undo"); see "Undo" in §8. |
| `RangeSlider`, `install_range_sliders`, `attach_range_slider` | Sliders beside bounded numeric inputs (see §9). |
| `BrandLogo`, `BrandMark`, `wordmark_html`, `app_icon` | The supplied logos and the logo's wordmark treatment (see §10). |
| `DeepLearningTrainingDialog`, `confirm_deep_learning_training` | The confirmation required before deep-learning training (see §11). |
| `size_stack_to_current_page(stack)` | Makes a `QStackedWidget`/`QTabWidget` as large as its current page only. By default it is as large as its largest page, even hidden ones. Used by the Models page so the labs fit 16:9 laptop screens. |
| `busy_state(button)` | Context manager for short synchronous computations: disables the button, changes its label to "Running…", shows the wait cursor and restores everything afterwards. Long computations belong in a worker thread instead. |
| `separator()`, `overline(text)` | Small layout helpers. |

`ExportBar.set_payload(frame_factory, figures, stem=…)` registers the current
result. The bar then runs the save dialogs itself: CSV via `frame_factory()`,
which is called only when the user exports, and HTML for one or several
figures (`save_figures_html` combines them into one standalone file).
`clear_payload()` disables the buttons again.

## 4. Offline chart rendering — `PlotView`

Every chart in the application is displayed through
`botorview.ui.components.PlotView`, a `QWebEngineView` subclass:

* The installed `plotly` package's `plotly.min.js` is written **once** to a
  per-user cache directory (`<tmp>/botorview-plots-<user>/plotly-<version>.min.js`).
* `set_figure(fig)` writes the figure as a small HTML page into the same
  directory. The page references the local bundle (`include_plotlyjs=<bundle name>`)
  and is then loaded. Charts therefore never depend on a CDN or network access,
  and the ~4.6 MB library is not re-embedded into each chart.
* Previous chart pages of a view are deleted when it is redrawn, and pages
  older than a day are removed from the cache.
* `show_message(text, detail="")` shows a themed placeholder page.
* Remote requests from chart pages stay blocked (the QtWebEngine default). The
  one exception is the Home study-area map (`allow_remote_resources=True`),
  whose OpenStreetMap tiles can only load with an internet connection. The UI
  states this in a caption.
* Plotly's image-download mode-bar button is removed, because QtWebEngine
  discards browser downloads without a download handler. PNG/SVG export would
  need either such a handler or the `kaleido` package, which is not installed.

## 5. Plotly template — `botorview/visualization/theme.py`

The `"botorview"` template (registered on import; made the default by
`apply_theme`) defines:

* typography;
* background colours;
* restrained gridlines;
* axis lines and outside ticks;
* left-aligned titles;
* legend, hover-label and colour-bar styling;
* default line width (1.5 px);
* table styling;
* the categorical, sequential and diverging colour scales.

Visualization modules pass `template=vt.TEMPLATE_NAME` and take colours from
named constants:

| Constant | Meaning |
|---|---|
| `PRIMARY` | Observed/primary series |
| `SECONDARY` | Highlighted events, fitted or predicted values |
| `NEUTRAL` | Thresholds and reference lines (dashed) |
| `EVENT_HIGH` / `EVENT_LOW` | Upper / lower extremes |
| `HIGHLIGHT_FILL`, `PRIMARY_FILL` | Translucent event and interval fills |
| `CATEGORICAL` | Groups such as regimes or data splits |
| `SEQUENTIAL` | Magnitudes |
| `DIVERGING` | Signed quantities centred on zero, e.g. correlation (negative = blue, positive = terracotta) |

Helpers:

* `vt.add_footnote(fig, text)` places scientific disclaimers a fixed distance
  below the plotting area and enlarges the bottom margin to fit them.
* `vt.style_subplot_titles(fig)` applies the standard subplot-title style.

These changes affect presentation only. No analysis definition, computed value
or plotted quantity was changed.

## 6. Model availability — `botorview/models/availability.py`

The UI lists some models that cannot currently be trained. A model is
*available* only when **both** of these hold:

* a training workflow for it is implemented in BotorView;
* its backend packages are installed (checked with `importlib.util.find_spec`,
  without importing them).

`botorview/ui/model_availability.py` presents this in the model selectors:

* Unavailable models remain visible but are **disabled** (greyed out), with the
  reason as a tooltip.
* If such a model is selected programmatically, an inline warning explains why,
  and the Train/Diagnostics actions are disabled.
* When PyTorch is missing, the deep-learning page says so, the lab disables
  training and shows the installation command (CPU build) and the PyTorch
  installation page for CUDA builds (`models/torch_backend: torch_missing_message`);
  `_run_training` also refuses to start.

As of this writing:

| Model(s) | Status |
|---|---|
| TBATS | Available: `tbats` is installed in the `climaxplore` environment (`classical` extra) |
| VARMAX, Exponential Smoothing State Space | Available: statsmodels |
| LSTM, GRU, BiLSTM | Available: PyTorch (CPU build) is installed in the `climaxplore` environment |

## 7. Application metadata — `botorview/app_info.py`

The version shown in the interface comes from the installed package metadata
(`pyproject.toml` → `0.1.0`), with a fallback to reading `pyproject.toml`.

The module is also the one place for global, non-visual settings:

* branding paths (`BRAND_BANNER_PATH`, `BRAND_ICON_PATH` under
  `botorview/assets/branding/`, declared as package data);
* the project links (`PROJECT_LINKS`: GitHub repository, documentation, paper,
  pretrained models). **They are placeholders** (`placeholder=True`): replace
  the URL and set `placeholder=False` when a resource is published — every link
  in the interface, including the pretrained-models recommendation before
  deep-learning training, reads this table;
* the citation (`CITATION_PLACEHOLDER`, clearly marked as a placeholder),
  the citation guidance and the suggested acknowledgement;
* PyTorch installation guidance (`PYTORCH_INSTALL_URL`, `PYTORCH_INSTALL_COMMAND_CPU`).
The technology list is built from the libraries that are actually installed.
Settings → System Information shows both. Help & About shows the version and
Python version and links there.

## 8. Information architecture

### Navigation bar

A single horizontal bar across the top of the window (`NavigationBar` in
`botorview/ui/navigation.py`) replaces the former vertical sidebar. From left
to right it holds:

* the logo (`BrandMark`: the square icon beside the banner, on both palettes);
* the workflow destinations, grouped by stage and separated by thin rules:
  * **Home**
  * **Data**: Data, Visualize (the page key and `NavBtn_Explore` keep the former name)
  * **Analysis**: Analysis
  * **Forecasting**: Preprocessing, Models, Model Comparison
* **Settings** and **Help & About**, at the right end.

A 3 px brand stripe in the logo's cyan, green and yellow (in thirds) runs under the bar.
The current page is marked by accent-coloured text and a 2 px underline.
Each button's tooltip names its group, describes the page and gives its
shortcut. **Ctrl+1 … Ctrl+9** open the destinations in bar order, and **F1**
opens Help & About. The buttons are not in the Tab order, so keyboard focus
never makes a second destination look selected.

Every button keeps its `NavBtn_<page name>` object name. The page key stays
`"Help"`, and the visible label is "Help & About". `MainWindow.sidebar` remains
as an alias of `MainWindow.navigation`, and `NavigationSidebar` as an alias of
`NavigationBar`. The Results placeholder is not in the navigation.

### Help & About

`botorview/ui/help_page.py`. The wide main column is the help:

* **Getting started**: six steps in workflow order (load, explore, analyse,
  prepare, train and evaluate, compare and export), each with a button that
  opens the page. The Analysis step lists the categories from
  `AnalysisPage.ANALYSIS_GROUPS`, so it cannot fall out of date.
* **Model availability in this installation**: generated from
  `models/availability.py`, with the reason for every unavailable model, and
  a note on the deep-learning backend (PyTorch version, CPU/CUDA, the training
  confirmation and the pretrained-models alternative).
* **Good to know**: short practical notes.

The narrower column (the columns stack on narrow windows) holds:

* **ABOUT BOTORVIEW**: the logo, a one-line description and the version,
  with a link to Settings → System Information.
* **Project links**: GitHub repository, Documentation (Read the Docs), the
  BotorView paper and Pretrained models, each tagged "Placeholder" while
  the resource is not public, with a note that the links are temporary.
* **Cite BotorView**: the citation guidance, the placeholder citation, a
  suggested acknowledgement sentence and **Copy Citation**.
* **Team BotorView**: every team member **once**, in publication order,
  with their roles (Developer, Science Support, Advisor) and their full
  affiliations written after the name, without affiliation numbers. The e-mail appears
  once, as "Contact". **Copy Attribution** copies the complete academic
  attribution (author order, affiliation numbers, all affiliations and the
  e-mail) as plain text.

The page ends with the tag "© BotorView-v1-2026" (`app_info.COPYRIGHT_TAG`).

The team data lives in `botorview/attribution.py` (no Qt), reproduced exactly
as provided by the team; `team_members()` derives the per-person view from it
without changing it. `tests/test_help_about.py` checks it line by line against
the project instructions.

### Workspace context

Every page that works on the active dataset shows the same
`WorkspaceContextBar` directly under its page header:

* Home
* Visualize
* Analysis
* Preprocessing
* Models
* Model Comparison

The Data page is the detailed metadata view itself, so it has no bar. When
the loader changed anything while reading the file, the Data page lists it
under the success message. For example: a NASA POWER header block skipped, date
columns combined into the index, fill values treated as missing, rows without a
timestamp removed, or repeated timestamps merged
(`core/data/loader.py: load_report_notes`).

**Changing or removing the dataset, with Undo.** While a dataset is loaded,
every context bar offers **Change dataset…** and **Remove**, and the Data page
offers **Load Another Dataset…** and **Remove Dataset**:

* Removing asks for confirmation, then returns every page to its no-dataset
  state (as **Clear Workspace** in Settings → Data & Workspace does) and opens
  the Data page.
* Loading another dataset while one is loaded asks first when Settings → Data
  & Workspace → "Confirm before replacing current dataset" is on (the
  default).
* After a removal, a replacement or Clear Workspace, the undo bar under the
  navigation bar offers **Undo**. It restores the dataset from the copy kept in
  memory (the file is not read again), and every page shows it again; results
  computed from it (analyses, preprocessing, unsaved models) are not restored.
  Undo is offered for the last change only and disappears when another dataset
  is loaded or the notice is dismissed.

**Preprocessing → Start Over** discards the applied missing-value handling and
preprocessing and returns the page's options to their defaults for the loaded
dataset, after a confirmation. Data already sent to Models stays there until
preprocessing is applied again.

The first line summarises the dataset: name, rows, columns, frequency and
period. It reads "No dataset loaded" when there is none. The second line is
page-specific:

| Page | Second line |
|---|---|
| Analysis | Active analysis and variable(s) |
| Visualize | Selected variable and visualization |
| Preprocessing | Whether processed data is ready or outdated |
| Models | Model input: raw dataset, or processed data from Preprocessing with target, feature count and split sizes |
| Home / Model Comparison | Source and study area |

Frequencies use one format throughout the interface, the pandas alias plus a
description (e.g. `D (daily)`), produced by `botorview/ui/formatting.py`.

`MainWindow._on_dataset_loaded` always passes a `DatasetMetadata` to the pages.
When a caller provides none, it is derived from the DataFrame with
`extract_metadata`.

### Analysis page

Categories are grouped by the question they answer
(`AnalysisPage.ANALYSIS_GROUPS`):

* **Temporal structure**: Trends, Seasonality, Wavelet, Stationarity, Change Points
* **Events**: Anomalies, Extremes
* **Relationships**: Correlations, Weather Regimes

Each group has its own colour from the logo — Temporal structure blue (cyan),
Events yellow, Relationships green (`AnalysisPage.GROUP_COLOURS`, from
`design_tokens.GROUP_COLOURS`; tokens `GROUP_<COLOUR>`, `_TEXT` and `_BG` in
both palettes, text contrast ≥ 5:1). The
group headers are tinted strips with a coloured bar, and the categories carry
the group colour in their left border and selected state. The overview shown
before a category is chosen uses the same colours.

`AnalysisPage.panels` maps each category to its panel. Adding an analysis
means adding one entry there and one in `ANALYSIS_GROUPS`.

Every analysis panel follows the same template:

1. Title and one-line purpose.
2. Parameter bar, with a tooltip for every parameter.
3. Run button, which shows a busy state while running (`busy_state`), or a
   progress bar and Cancel button for analyses that run in a worker thread.
4. Inline validation or error message.
5. Results: an export bar (CSV and HTML), a summary, and the figure(s).
6. A collapsed **Method & assumptions** section.

The Method & assumptions texts live in `botorview/ui/analysis_notes.py`.
They describe what each `core.analysis` module computes, its defaults, its
missing-value handling and its limitations. They must be kept in step with
the implementation.

The CSV tables are built by `botorview/io/analysis_export.py`, which is pure
pandas with no Qt. These functions only reshape values the analysis already
computed:

| Analysis | CSV content |
|---|---|
| Trends | One row of statistics per method; slopes are per valid observation |
| Seasonality | Observed, trend, seasonal and residual components |
| Anomalies | Value and anomaly flag per observation |
| Correlations | Variable pairs with coefficient and valid-observation count |
| Stationarity | ADF statistics, then ACF/PACF by lag with confidence bounds |
| Change Points | Value, score and change-point flag per observation |
| Extremes | Event table with the threshold(s) |
| Weather Regimes | Regime label per observation |
| Wavelet | Global spectrum: one row per period with background, significance levels and COI-free fraction. A separate button exports the full power grid (one row per time step and period, with the local significance ratio and a cone-of-influence flag); it asks for confirmation above 500,000 rows |

### Models page

The Models page has the standard page header and the workspace context bar,
then one tab per model family: Statistical Models, Machine Learning, Deep
Learning and Pretrained Models. Inside a family, a lab's workflow is a
numbered **step list** on the left (`StepTabWidget`), not another row of tabs.

**One step vocabulary.** Step names come from `botorview/ui/lab_steps.py`,
so the same kind of step has the same name in every lab. Each lab lists the
steps it implements, in this order, and each step's tooltip describes it:

| Lab | Steps |
|---|---|
| ARIMA, SARIMA, Prophet | Configure & Train · Validate · Compare Candidates · Final Test · Diagnostics · Forecast · Save |
| Dynamic Harmonic Regression | Configure · Harmonics · Train · Evaluate · Forecast · Save |
| TBATS, VARMAX, Exponential Smoothing State Space | Configure · Train · Evaluate · Diagnostics · Forecast · Save |
| Machine learning (XGBoost, LightGBM, CatBoost) | Data · Features · Feature Selection · Split · Configure · Train · Evaluate · Diagnostics · Forecast · Save |
| Deep learning (LSTM, GRU, BiLSTM) | Data · Features · Sequences & Split · Configure · Train · Evaluate · Diagnostics · Forecast · Save |

*Validate* means validation-period metrics compared with naive and drift
baselines. *Final Test* is the single evaluation on the held-out test period
after the configuration is locked. *Evaluate* shows the training, validation
and test periods together, for labs without a lock step.

The TBATS, VARMAX and ETS labs share one implementation,
`botorview/ui/statistical_model_lab.py: SimpleStatisticalLab`; each model's
lab (`tbats_model_lab.py`, `varmax_model_lab.py`, `ets_model_lab.py`) adds only
its Configure form, its configuration and its adapter. They are trained by the
common statistical contract (`models/training/{tbats,varmax,ets}_trainer.py`,
through `TrainerWorker`). Their Evaluate step lists the naive and drift
baselines with the model, and their Forecast step fits the chosen
configuration again on the whole series in a worker thread before
forecasting beyond the last observation.

**Model input.** The statistical labs show the model facts and the
chronological split in a `ChronologicalSplitView` ("Model Input"). The
periods come from the function the trainers use, so the summary always
matches the split used for training.

The machine-learning lab splits after feature engineering: lagged and rolling
features remove the first rows. Its Split step therefore shows the periods
from the training result's split summary once the model is trained. The
deep-learning Sequences & Split step shows the preprocessing periods its
sequences are built from.

The Data step of the machine-learning lab keeps target and time-column
selection and the checks, with a pass/issues message. It no longer repeats the
data preview, since the dataset is described by the context bar and on the
Data page.

**One results layout.** Every lab shows metrics in a `MetricsTable` above its
charts. Validate lists the model and the two baselines on the validation
period. Final Test has its own table for the test period, instead of
appending a row to the validation table. Evaluate lists training, validation
and test. Missing or undefined values show as "—".

**One save format.** Every lab's Save step writes a `.botor` package through
`botorview/ui/model_saving.py` and `botorview/models/export.py`, with a
model-name field and the same button, note and confirmation. The package
follows `docs/model_artifact_contract.md` and can be imported under Pretrained
Models. The machine-learning lab keeps its metadata JSON and metrics CSV
exports under "Other exports".

**Width.** Each lab and step is only as wide as the page on screen
(`size_stack_to_current_page`), so the labs fit a 1366 × 768 laptop without
horizontal scrolling.

### Background analyses — `botorview/ui/workers/analysis_worker.py`

The existing panels compute synchronously inside `busy_state`. Wavelet
Analysis can take tens of seconds (mostly the Monte Carlo test), so it runs in a
worker thread:

* `AnalysisWorker(function, *args, cancel_exceptions=(), **kwargs)` calls
  `function(*args, progress=…, should_cancel=…, **kwargs)` on a `QThread`, using
  the same QObject + `moveToThread` pattern as the training workers. It emits
  `progress(fraction, message)`, then exactly one of `finished(result)`,
  `error(message)` or `cancelled()`. `cancel()` sets a flag that the analysis
  polls; it raises one of `cancel_exceptions` to stop.
* `start_worker(worker, on_thread_finished)` starts the thread. The caller keeps
  references to the worker and thread until `on_thread_finished` runs; releasing
  them earlier deletes objects the thread still uses.
* The panel connects the worker signals to its own methods (so they run on the
  GUI thread), keeps Run disabled until the previous thread has ended, discards
  the outcome of a run whose dataset was replaced, and connects
  `shutdown()` to `QApplication.aboutToQuit` so that closing the application
  during a run stops the thread cleanly.
* `run_in_background = False` runs the same code synchronously (used by tests).

The scientific method is documented in `docs/wavelet_analysis.md`.

## 9. Range sliders — `botorview/ui/components/range_slider.py`

Bounded numeric parameters have a slider beside the spin box, so a value can
be dragged or typed exactly. `MainWindow` calls `install_range_sliders(self)`
once; widgets that build spin boxes later (the wavelet parameters, which
depend on the chosen wavelet) call `attach_range_slider` themselves.

* The spin box keeps its object name, signals, range, step, default and
  position in its layout; it is the source of truth.
* Sliders in inline rows (several parameters in one horizontal row) are
  narrower (56–180 px instead of 96–320 px), so the row still fits beside a
  lab's step list. Model orders (ARIMA and SARIMA p, d, q, P, D, Q, s) are laid
  out two per row.
* **Scale.** Linear, snapped to the spin box's single step. Ranges over
  several orders of magnitude (minimum > 0 and maximum / minimum ≥ 500 — e.g.
  learning rate, epochs, batch size, number of trees) use a logarithmic
  scale with values rounded to two significant figures. `set_slider_range(spin,
  scale="log")` forces it (deep-learning layer width).
* **Practical range.** `set_slider_range(spin, maximum=…)` narrows the slider
  while the spin box keeps its own bounds (Preprocessing sequence length and
  horizon: the slider covers 730 and 365 steps; larger values can still be typed).
* **Not given a slider:** random seeds (identifiers, opted out with
  `opt_out_of_slider`), effectively unbounded inputs (more than 100 000 linear
  steps, e.g. the constant used for imputation), spin boxes in table cells,
  and the placeholder forms of models that are not implemented yet.
* **Synchronisation.** Typing moves the slider. Dragging updates the spin box
  display live and emits `valueChanged` once, on release, so charts that
  follow a parameter are not recomputed for every pixel. The slider follows
  the spin box's enabled state, visibility and tooltip, and ignores the mouse
  wheel unless it has focus (scrolling a page never changes a value).

No application-wide Python event filter is used: PySide can crash when such
a filter sees objects that are being created or destroyed. For the same
reason, Settings → General hides tooltips with a stylesheet rule
(`theme.set_tooltips_hidden`) rather than an event filter.

## 10. Branding — `botorview/ui/components/branding.py`

The supplied logos are used as they are (byte-identical copies of
`Logo_Baner.png` and `Logo_Square.png` in `botorview/assets/branding/`, named
`botorview_banner.png` and `botorview_icon.png`): the banner (the name and the
tagline "Explore | Analyze | Predict", `app_info.APP_TAGLINE`) and the square
icon. They are scaled
smoothly for the screen's pixel ratio, so they stay crisp.

* **Navigation bar:** `BrandMark` at the bar height: the square icon beside
  the banner. The banner's white lettering has a navy outline on a transparent
  background, so it is readable on both palettes.
* **Home:** a larger `BrandMark` heads the landing page; the active workspace
  header reads "Welcome to" followed by the wordmark.
* **Help & About:** the logo heads the About block.
* **Window and task-bar icon:** `app_icon()` from the square logo.

`wordmark_html()` writes the name as the logo does: heavy "Botor" and "iew"
around a cyan "V".

## 11. Preferences — Settings → General (`botorview/ui/preferences.py`)

| Setting | Key in `settings.json` | Applies |
|---|---|---|
| Theme: Light, Dark or Same as the system | `appearance` | Immediately |
| Text size: 90 / 100 / 115 / 130 / 150 % | `interface_scaling` | Immediately |
| Reopen at the last window size and position | `window_restore` (`window_geometry` holds it) | At the next start |
| Show explanatory tooltips | `show_tooltips` | Immediately |
| Startup page | `startup_page` | At the next start |

At start-up, theme and text size are selected by `apply_startup_preferences`
before any page or chart is created. A change in Settings is applied to the
running application, without a restart, by `botorview/ui/appearance.py:
change_appearance`:

1. the design tokens switch palette and text scale (`use_palette`,
   `use_text_scale`) and the Plotly template is rebuilt
   (`visualization.theme.refresh`);
2. `apply_theme(force=True)` installs the new Qt palette, font and
   stylesheet;
3. values that widgets captured when they were built are updated by
   `recolour_widgets`: an `AppearanceChange` maps every old colour and font
   size to the new one and rewrites rich-text labels, text areas, table items
   and the figures of `PlotView`s (`PlotView.refresh_appearance`);
4. widgets whose sizes depend on the text size re-measure themselves in a
   `refresh_appearance(change)` hook (navigation bar height and logo, step
   lists, `ResponsiveColumns`, the Analysis category list).

The dataset, results and charts stay on screen. Re-applying the stylesheet
to every widget takes a few seconds, so Settings shows a busy cursor and
"Applying the new appearance…" meanwhile. With *Same as the system*, a change
of the desktop's colour scheme is followed as well (`follow_system_scheme`).

## 12. Deep-learning training confirmation — `ui/components/training_confirmation.py`

Before a deep-learning model is trained, `DLModelLab` shows
`DeepLearningTrainingDialog`:

* a prominent warning that training can require substantial CPU/GPU, RAM/VRAM,
  storage and computation time, and that cancelling keeps no partial model;
* the size of the planned run (`TrainingPlan`): model, trainable parameters,
  training and validation sequences, maximum epochs, batch size and batches per
  epoch, maximum number of weight updates, compute device, and the memory of
  the sequence data and of the weights;
* a recommendation to try a pretrained model first, with the (placeholder)
  pretrained-models link from `app_info`.

"Start Training" is enabled only after the user ticks the acknowledgement,
and Cancel is the default button. Training starts only when the dialog was
accepted with the acknowledgement ticked. The Train step also says, before
the user starts, that a confirmation will be asked. The PyTorch backend itself
is described in `docs/deep_learning.md`.
