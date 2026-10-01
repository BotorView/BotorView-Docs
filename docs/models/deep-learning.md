# Deep-learning models

**Models → Deep Learning** trains recurrent neural networks — **LSTM**, **GRU** and
**BiLSTM** — with PyTorch on input windows of the preprocessed data. The implementation is
described in detail in {doc}`../deep_learning`.

```{important}
Training a network can take a long time and a lot of memory. Before every run the lab shows
the size of the run (parameters, samples, epochs, weight updates, device, memory) and starts
only after you confirm. Consider a pretrained model first ({doc}`pretrained`).
```

## Input windows

Each sample is a window of $L$ past time steps of the features, $X_i \in \mathbb R^{L\times F}$,
and the next $H$ target values (see {doc}`../user-guide/preprocessing`). The windows come from
**Preprocessing** or are built in the lab's **Sequences & Split** step (*Lookback* $L$,
default 30; *Forecast Horizon* $H$, default 1). Features are scaled with statistics of the
training period.

## Networks

An LSTM cell updates a hidden state $h_t$ and a cell state $c_t$ at every step of the window:

$$
\begin{aligned}
i_t &= \sigma(W_i x_t + U_i h_{t-1} + b_i), &
f_t &= \sigma(W_f x_t + U_f h_{t-1} + b_f), \\
o_t &= \sigma(W_o x_t + U_o h_{t-1} + b_o), &
\tilde c_t &= \tanh(W_c x_t + U_c h_{t-1} + b_c), \\
c_t &= f_t \odot c_{t-1} + i_t \odot \tilde c_t, &
h_t &= o_t \odot \tanh(c_t),
\end{aligned}
$$

with the input, forget and output gates $i_t, f_t, o_t$. A **GRU** uses two gates (update and
reset) and no separate cell state. A **BiLSTM** also reads the window backwards and merges
both directions (concatenation, sum, average or product). The output layer maps the final
hidden state to the $H$ forecast values.

| Setting | Default |
|---|---|
| Network Depth | 2 recurrent layers (1–3) |
| Base Units (per layer) | 64 |
| Dropout | 0.2 |
| Epochs, Batch Size | 30, 32 |
| Learning Rate, Optimizer | 0.001, Adam (AdamW, RMSprop, SGD) |
| Early stopping | on (patience 15 epochs, best weights restored) |
| Reduce LR on Plateau | on (factor 0.5 after 5 epochs without improvement) |

## Training and evaluation

The weights minimise the mean squared error on the training windows; batches are taken in
time order. The validation windows only **monitor** the training — for early stopping and the
learning-rate reduction — and never update the weights. The metrics of the training,
validation and test periods are computed in the original units of the target (see
{doc}`evaluation`).

The compute device is chosen automatically (NVIDIA GPU, Apple silicon or CPU); the random
seed makes runs reproducible on the same hardware and PyTorch build.
