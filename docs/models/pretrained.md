# Pretrained models and model packages

## Saving a model

The **Save** step of every lab writes a **`.botor` package**: a zip archive with the model file
and a `metadata.json` describing it — model type, framework, target, features (in order),
frequency, the model settings, the sizes of the training, validation and test periods, the
metrics, and the preprocessing used. The exact format is the
{doc}`../model_artifact_contract`.

## Importing a model

**Models → Pretrained Models → Import Model** accepts BotorView packages (`.botor`, and
`.climax` packages written under the project's former name) and raw model files (`.pkl`,
`.joblib`, `.pt`, `.keras`, `.h5`).

1. The file is **inspected** first — its metadata, compatibility, warnings and errors are
   shown. Nothing is loaded or executed at this stage.
2. **Register Model** adds it to the **Model Library**.
3. **Load Model** loads it; **Activate Model** makes it the active model of the workspace.

BotorView never infers what a model needs (target, features, sequence length, scaling) from
its file name: this information must be in the package metadata.

```{warning}
`.pkl` and `.joblib` files can execute code when they are loaded. Import them only from
sources you trust. PyTorch files written by BotorView contain plain data and are read safely.
```

Legacy Keras models (`.keras`, `.h5`) need TensorFlow (`pip install "botorview[keras-import]"`).

## Published pretrained models

Pretrained models will be published in the project's repository; the link will be added here
when the repository is public.
