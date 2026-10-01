# Loading data

**Data** ({kbd}`Ctrl+2`) loads a dataset and describes it. **Browse Files** opens a CSV file
(comma-separated, one row per time step).

## What happens while reading

BotorView reads the file in this order and reports every change under
*While reading the file*:

1. **NASA POWER header** — a header block starting with `-` and ending with `-END HEADER-` is
   skipped. When the header states a fill value (for example *"The value −999 indicates a
   missing value"*), cells equal to it are treated as missing. A plain CSV that contains −999
   keeps the value as it is.
2. **Date parts** — in NASA POWER files, the columns `YEAR`, `MO`, `DY` (and `HR`) or `YEAR`,
   `DOY` are combined into one `date` column.
3. **Time index** — text columns are converted to dates where possible; the first date column
   becomes the time index and the rows are sorted by time. Rows without a valid date are
   removed. Without any date column the rows are numbered.
4. **Duplicate timestamps** — rows with the same timestamp are merged: numeric values are
   averaged, other values take the first row's value.
5. **Numbers** — the remaining text columns are converted to numbers where possible.

NASA POWER *monthly/annual* files (one row per parameter and year) are recognised and
rejected with an explanation, because they are not a time series in rows.

## What the page shows

* **Dataset Information** — file name, source (NASA POWER when the header says so), study
  area and coordinates (from the header or constant latitude/longitude columns), frequency,
  start and end date, rows, columns and parameters.
* **Frequency** — inferred from the timestamps, for example *D (daily)* or *MS (monthly)*;
  irregular timestamps show *Irregular/Unknown*.
* **Data Quality** — missing cells, duplicate timestamps, numeric and non-numeric columns.
* **Preview** — the first 10 rows; missing values are shown dimmed.

Missing values are not filled when the data are loaded. Each analysis states how it treats
them, and **Preprocessing** handles them for forecasting.

## Replacing and removing a dataset

**Load Another Dataset…** replaces the dataset (after a confirmation, see
{doc}`settings`) and **Remove Dataset** clears the workspace. Both can be undone from the
notice under the navigation bar. **Continue to Visualize →** moves on.
