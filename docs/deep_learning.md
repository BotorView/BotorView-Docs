# Deep-learning models (PyTorch backend)

BotorView's deep-learning forecasters — **LSTM**, **GRU** and **BiLSTM** —
are implemented with PyTorch in `botorview/models/torch_backend/`. The
earlier TensorFlow/Keras implementation (`models/lstm`, `models/gru`,
`models/bilstm`) is kept for importing legacy `.keras` models only.

## Requirements

* **PyTorch ≥ 2.2** (`pyproject.toml` extra `deep-learning`). The `climaxplore`
  Conda environment has the CPU build (`environment.yml`).
* A GPU is optional. The compute device is chosen automatically: CUDA when
  PyTorch sees an NVIDIA GPU, Apple Metal (MPS) on Apple silicon, otherwise
  the CPU. The Deep Learning page shows the device and the PyTorch version.
* Sequences built in Preprocessing (or in the lab's Sequences & Split step).

When PyTorch is missing, nothing fails silently: the Deep Learning page says
so, training is disabled, and the message gives the installation command for
the CPU build and the PyTorch installation page for CUDA builds
(`torch_backend.torch_missing_message`, text in `app_info`). The model
catalogue (`models/availability.py`) lists the models as unavailable with the
reason, and Help & About shows the same.

## Architecture — `network.py: RecurrentForecaster`

The network mirrors the earlier Keras models:

* stacked recurrent layers (`nn.LSTM` or `nn.GRU`), one per entry of
  `config.units`; BiLSTM layers are bidirectional and their two directions
  are merged by `merge_mode` (`concat`, `sum`, `ave` or `mul`);
* dropout (`config.dropout`) on the input of every recurrent layer, with one
  mask per sequence shared by all time steps, as in Keras;
* a dense output layer on the last time step, with one output per forecast
  step (`forecast_horizon`).

Two Keras settings have no PyTorch equivalent and are **not** applied:
`recurrent_dropout` and a non-`tanh` `activation`. When a configuration sets
them, the training log says so (`training.unsupported_settings`).

## Training — `training.py: train_recurrent_network`

* **Chronological batches.** The data loader does not shuffle. The inputs are
  the sequences built after the chronological training / validation / test
  split, with imputation and scaling fitted on the training period only
  (Preprocessing).
* **Validation is monitoring only.** The validation period never updates the
  weights. It is used for early stopping (`early_stopping_patience`,
  `early_stopping_min_delta`), for reducing the learning rate on a plateau
  (`reduce_lr_factor`, `reduce_lr_patience`, `reduce_lr_minimum`) and to
  restore the weights of the epoch with the lowest validation loss.
* **Optimisers and losses:** Adam, AdamW, RMSprop, SGD; MSE, MAE (L1), Huber.
* **Reproducibility.** `random_seed` seeds NumPy and PyTorch. Results are
  reproducible on the same hardware and PyTorch build; GPU kernels can differ
  slightly between devices.
* **Inputs are validated** before any computation: array shapes, matching
  validation shape, and no NaN or infinite values.
* **Cancellation.** `should_stop()` is checked before every batch; cancelling
  raises `TrainingCancelled` and no partial model is kept.

The lab runs training in a worker thread (`ui/workers/dl_workers.py`), so the
interface stays responsive; progress (loss and validation loss per epoch),
early stopping and any unsupported settings are reported in the Train step.

## Confirmation before training

Deep-learning training can require substantial CPU/GPU capacity, RAM/VRAM,
storage and time. Before every run the lab shows a confirmation with the size
of the run (parameters, sequences, epochs, batches, weight updates, device,
memory of data and weights) and a recommendation to try a pretrained model
first (`docs/ui_design_system.md` §12). Training starts only after the user
ticks the acknowledgement and presses Start Training.

## Pretrained models

Pretrained models are to be published in the project's GitHub / Hugging Face
repository. The address is a **placeholder** for now, defined once in
`botorview/app_info.py` (`PROJECT_LINKS`, key `pretrained`); replace it there
when the repository is public. Models are imported under
**Models → Pretrained Models**.

## Saving and loading

Trained networks are saved as `.pt` files inside `.botor` packages; the file
format (a plain dictionary read with `weights_only=True`) is described in
`docs/model_artifact_contract.md`. The adapters (`adapter.py`) implement the
common `BaseModelAdapter` interface and are registered under the model types
`lstm`, `gru` and `bilstm`.

## Testing

`tests/test_torch_backend.py` covers the network, the adapters, saving and
loading, input validation and cancellation. It does not train a network:
cancellation is tested before the first batch.
