# Installation

BotorView is a Python desktop application (PySide6 / Qt). It runs on Linux, Windows and
macOS with Python 3.10–3.12.

## With Conda (recommended)

The repository contains the complete, tested environment in `environment.yml`
(the environment is called `climaxplore`, the project's former name):

```bash
conda env create -f environment.yml
conda activate climaxplore
```

The environment installs BotorView itself in *editable* mode from the repository, so
changes to the source are used immediately.

## With pip

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[classical,ml,deep-learning]"
pip install PySide6
```

The optional groups (*extras*) add model families:

| Extra | Installs | Enables |
|---|---|---|
| `classical` | statsmodels, Prophet, tbats | ARIMA, SARIMA/SARIMAX, Prophet, DHR, TBATS, VARMAX, ETS, stationarity and decomposition analyses |
| `ml` | XGBoost, LightGBM, CatBoost | the machine-learning forecasters |
| `deep-learning` | PyTorch | LSTM, GRU and BiLSTM |
| `keras-import` | TensorFlow | importing legacy Keras (`.keras`) models only |

A model family whose packages are missing stays visible in the application, disabled, with
the reason and the installation command.

### PyTorch builds

The `deep-learning` extra installs the default PyTorch build for your platform. For the
CPU-only build (smaller download):

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

For an NVIDIA GPU, choose the matching command at <https://pytorch.org/get-started/locally/>.

## Starting BotorView

```bash
python -m botorview
```

On first start the window opens as a 16:10 window that fills the height of the screen.
Settings are stored in `~/.botorview/settings.json` (settings of the former ClimaXplore
folder `~/.climaxplore` are taken over automatically).
