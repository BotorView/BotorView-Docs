# BotorView Model Artifact Contract

This document defines the production-grade artifact contract for models trained externally (e.g., Google Colab, Kaggle) that are to be imported into BotorView.

## Core Principle

**BotorView must NEVER infer critical model requirements from filenames.**
All metadata must be explicitly defined in a structured format (e.g., `metadata.json`) within the `.botor` package or provided as a sidecar for raw artifacts.

## Artifact Structure

The recommended project structure for a `.botor` bundle is:

```
bundle.botor (or directory)
├── metadata.json           # REQUIRED: The core metadata contract
├── model/                  # REQUIRED: The actual trained model artifact (e.g., model.pt, model.joblib, model.keras)
└── preprocessing.joblib    # OPTIONAL: Serialized preprocessing objects
```

## Minimum Metadata Contract (`metadata.json`)

Metadata is divided into strict requirements for basic import/compatibility, and optional informational fields.

### Required Fields (for all models)

*   `name` (str): Human-readable name of the model.
*   `model_type` (str): The specific model adapter type (e.g., `random_forest`, `xgboost`, `lstm`, `gru`).
*   `framework` (str): The training framework used (e.g., `sklearn`, `xgboost`, `pytorch`, `tensorflow`, `keras`).
*   `version` (str): Model version (defaults to `"1.0"`).

### Recommended / Runtime Requirement Fields

These fields drive compatibility checking. Missing critical requirements result in an `UNKNOWN` compatibility state instead of silently upgrading.

*   `target` (str): The exact target variable the model predicts.
*   `features` (list[str]): The exact ordered list of expected input features.
*   `frequency` (str): Time series frequency the model expects (e.g., `D` for daily).
*   `input_shape` (list[int]): Shape of the input tensor (e.g., `[30, 10]`).
*   `sequence_length` (int): Number of timesteps required in the input window for sequence models.
*   `forecast_horizon` (int): Number of timesteps the model predicts into the future.
*   `preprocessing` (dict): Preprocessing requirements (see Preprocessing Contract below).

### Optional Informational / Training Fields

*   `training_info` (dict): Details about the training setup (e.g., dataset, epochs, environment).
*   `metrics` (dict): Evaluation metrics captured during testing (e.g., `MAE`, `RMSE`, `R2`).
*   `description` (str): General notes or summary of the model.
*   `model_file` (str): Relative path to the model artifact within the bundle.

## Model-Family-Specific Requirements

Different model architectures have different baseline requirements to pass compatibility:

### Tabular Models (Random Forest, XGBoost)
*   **Required**: `target`, `features`
*   **Optional**: `preprocessing` (e.g., if specific scaling was used during training)
*   **Prohibited**: Cannot accept 3D sequence tensors.

### Sequence/Recurrent Models (LSTM, GRU, RNN)
*   **Required**: `target`, `features`, `sequence_length`
*   **Highly Recommended**: `input_shape`, `forecast_horizon`
*   **Optional**: `preprocessing`

## Preprocessing Contract

The preprocessing applied during inference **must exactly match** the preprocessing used during training.
The `preprocessing` dictionary in `metadata.json` captures this state.

**Key Preprocessing Fields:**
*   `scaling_method` (str): Scaling strategy used (e.g., `MinMaxScaler`, `StandardScaler`).
*   `imputation_strategy` (str): How missing values were handled (e.g., `forward_fill`, `mean`).

BotorView's compatibility engine compares the active preprocessing execution state against the model's requested preprocessing state. Mismatches result in `INCOMPATIBLE`.

## Security Considerations (Safe Serialization)

*   **Raw Pickle/Joblib Artifacts**: These formats are inherently unsafe and can execute arbitrary code upon deserialization.
*   BotorView **will not** automatically deserialize raw `.pkl` or `.joblib` models without explicit trust verification.
*   The system uses safe introspection on metadata first. If a raw file lacks metadata, a warning is emitted about the trust requirement before proceeding with adapter-based loading.

## Packages written by BotorView

Every model lab saves a trained model the same way: the **Save** step writes a
`.botor` package through `botorview/models/export.py: save_model_package`.
The package is a zip archive with `metadata.json` and the model file at its
root, as described above, so it can be imported under **Models → Pretrained
Models**.

| Lab | `model_type` (adapter) | `framework` | Model file |
|---|---|---|---|
| ARIMA | `sarima` | `statsmodels` | `model.joblib`: the fitted statsmodels result. ARIMA is the non-seasonal case of SARIMA, and the SARIMA adapter loads it. `training_info.model` is `"ARIMA"`. |
| SARIMA / SARIMAX | `sarima` | `statsmodels` | `model.joblib`: the fitted statsmodels result; exogenous predictors are listed in `features` and `training_info.exogenous`. |
| Prophet | `prophet` | `prophet` | `model.joblib`: the fitted Prophet model; regressors are listed in `features` and `training_info.regressors`. |
| Dynamic Harmonic Regression | `dhr` | `statsmodels` | `model.joblib`: the DHR adapter state (fitted result, order, seasonal period, Fourier terms). |
| XGBoost / LightGBM / CatBoost | `xgboost` / `lightgbm` / `catboost` | same as `model_type` | `model.joblib`: `(native model, feature list)`, the bundle the adapters load. The feature-engineering settings are in `training_info.feature_config`; inputs must be derived the same way before prediction. |
| Exponential Smoothing State Space (ETS) | `ets` | `statsmodels` | `model.joblib`: the fitted-state dictionary described below. |
| TBATS | `tbats` | `tbats` | `model.joblib`: the fitted-state dictionary described below. |
| VARMAX | `varmax` | `statsmodels` | `model.joblib`: the fitted-state dictionary; `endogenous` lists all modelled series (the target first), `exogenous` the regressors. |
| LSTM / GRU / BiLSTM | `lstm` / `gru` / `bilstm` | `pytorch` | `model.pt` (see below); `sequence_length`, `forecast_horizon` and `input_shape` are set, and `training_info` records the backend, the configuration and the number of epochs run. |

What the labs record in `metadata.json`:

* `name`: the name typed in the Save step, or `<model>_<target>_<timestamp>`.
* `target`, `features` (ordered), and `frequency` (the pandas alias detected
  from the data, e.g. `D`).
* `training_info`: the model settings read from the fitted object where
  possible (for example the statsmodels `order`, `seasonal_order` and
  `trend`), the observation counts of the chronological training, validation
  and test periods, and the split method.
* `metrics`: flat keys `<period>_<metric>`, where the period is `training`,
  `validation` or `test` and the metric is `mae`, `rmse`, `mse`, `mape`, `r2` or
  `mean_error` (actual minus forecast). Non-finite values are omitted.
* `preprocessing`: for models trained on data from the Preprocessing page,
  `scaling_method` and `imputation_strategy`.

**Fitted-state files (ETS, TBATS, VARMAX).** These adapters
(`botorview/models/fitted_state.py: FittedStateAdapter`) write a joblib
dictionary with `format` = `"botorview-statistical-state"`, `model_type`, the
fitted results object (`model`), the configuration (`config`), `target`,
`endogenous`, `exogenous`, `training_rows` and `metadata`. A file without the
format marker, or with another `model_type`, is rejected. The saved model is
the one fitted on the training period (the Forecast step's refit on all data
is not saved). Because the file contains a pickled results object, the
trust rules for joblib files above apply.

**Legacy files.** Packages written under the project's former name keep
working: the `.climax` extension is accepted next to `.botor`
(`ModelPackage.LEGACY_PACKAGE_EXTENSIONS`), and `.pt` files with the format
marker `"climaxplore-recurrent"` are loaded like `"botorview-recurrent"`
files. New files always use the BotorView names.

**Loading.** `ModelManager.load_model_artifact` resolves a package to the
model file named in `metadata.json` before calling the adapter's `load`. An
archive is extracted to a temporary directory, which is removed after loading.
Raw model files are loaded directly, as before.

## Deep-learning model files (`.pt`)

The LSTM, GRU and BiLSTM adapters (`botorview/models/torch_backend/adapter.py`)
save a PyTorch file holding **a plain dictionary, not a pickled Python object**:

| Key | Content |
|---|---|
| `format`, `format_version` | `"botorview-recurrent"`, `1` |
| `model_type` | `lstm`, `gru` or `bilstm` |
| `architecture` | The arguments that rebuild the network: `n_features`, `hidden_units`, `output_units`, `cell`, `bidirectional`, `merge_mode`, `dropout` |
| `state_dict` | The weights |
| `config` | The training configuration (`LSTMConfig` / `GRUConfig` / `BiLSTMConfig` fields) |
| `input_shape` | `[sequence_length, features]` |
| `history` | Per-epoch `loss`, `val_loss` and learning rate |
| `torch_version` | The PyTorch version that wrote the file |

Files are read with `torch.load(..., weights_only=True)`, which does not
execute code. A file without the `format` marker, or with another
`model_type`, is rejected with an explanation; the adapter does not guess
the architecture from the weights. `.pth` is accepted as a synonym.

Legacy Keras (`.keras`) models remain importable through the TensorFlow
adapters when TensorFlow is installed (`pip install "botorview[keras-import]"`);
without it, the import reports the missing dependency.
