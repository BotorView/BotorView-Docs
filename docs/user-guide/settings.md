# Settings

**Settings** ({kbd}`Ctrl+8`) are saved in `~/.botorview/settings.json` and kept between
sessions. **Restore Default Settings** resets them (datasets, models and results are not
affected).

## General

| Setting | Effect |
|---|---|
| Theme | Light, Dark, or Same as the system. Applies immediately. |
| Text size | 90 %, 100 %, 115 %, 130 % or 150 % for all text, including charts and tables. Applies immediately. |
| Window size at start-up | Reopen at the last size and position, or (off) open as a 16:10 window fitted to the screen. |
| Tooltips | Show short explanations when the pointer rests on a control. |
| Startup page | Home, Data, Analysis or Models. |

Changing the theme or text size re-styles the running application without a restart; the
dataset, results and charts are kept. This takes a few seconds, during which the pointer shows
a busy cursor.

## Data & Workspace

| Setting | Effect |
|---|---|
| Auto-validate imported datasets | Saved preference. |
| Confirm before replacing current dataset | Ask before a new file replaces the loaded dataset. |
| Clear Current Workspace | Removes the dataset from the workspace (can be undone); files on disk are not touched. |

## Modeling Defaults

**Random Seed** (default 42) and **Default Forecast Horizon** (default 30 steps) are saved as
preferences. The labs have their own seed and horizon fields with the same defaults.

## Export & Files

The save dialogs for exported charts, tables and model packages open in the **export
directory** when it exists (default `~/Documents/BotorView_Exports`). **Change…**, **Open
Directory** and **Restore Default Location** manage it.

## System Information

The versions of BotorView, Python and the scientific libraries in use; optional libraries
that are not installed are listed with what they would enable.
