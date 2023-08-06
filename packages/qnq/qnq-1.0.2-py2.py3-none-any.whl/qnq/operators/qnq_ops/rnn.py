# reference: https://github.com/pytorch/pytorch/
# commit 5233ff9f159b23649c714bcc643a82192e2d94b1
import math
import warnings
import numbers
from typing import List, Tuple, Optional, overload

import torch
import torch.nn as nn
from torch import Tensor, transpose
from torch.nn.parameter import Parameter
from torch.nn.utils.rnn import PackedSequence

from .torchfunc import *


def apply_permutation(tensor: Tensor,
                      permutation: Tensor,
                      dim: int = 1) -> Tensor:
    return tensor.index_select(dim, permutation)


# REF: https://github.com/pytorch/pytorch/blob/master/benchmarks/fastrnns/cells.py
class QNQGRU(nn.Module):
    def __init__(self,
                 input_size,
                 hidden_size,
                 num_layers,
                 bias: bool = True,
                 num_directions=1,
                 batch_first=False):

        super().__init__()
        self.batch_first = batch_first
        gate_size = 3 * hidden_size
        self.num_layers = num_layers
        self.num_directions = num_directions

        self.params = []

        for layer in range(num_layers):
            for direction in range(num_directions):
                layer_input_size = input_size if layer == 0 else hidden_size * num_directions

                w_ih = Parameter(torch.Tensor(gate_size, layer_input_size))
                w_hh = Parameter(torch.Tensor(gate_size, hidden_size))
                b_ih = Parameter(torch.Tensor(gate_size))
                # Second bias vector included for CuDNN compatibility. Only one
                # bias vector is needed in standard definition.
                b_hh = Parameter(torch.Tensor(gate_size))
                layer_params = (w_ih, w_hh, b_ih, b_hh)

                suffix = '_reverse' if direction == 1 else ''
                param_names = ['weight_ih_l{}{}', 'weight_hh_l{}{}']
                if bias:
                    param_names += ['bias_ih_l{}{}', 'bias_hh_l{}{}']
                param_names = [x.format(layer, suffix) for x in param_names]

                for name, param in zip(param_names, layer_params):
                    setattr(self, name, param)
                # add param_names in self.params for one line
                self.params.extend(param_names)

        # copy parameter to here
        for id in range(num_layers):
            setattr(self, 'gates_mm_' + str(id) + '_ih',
                    TorchDummy())  # gates_matmal_ih
            setattr(self, 'gates_mm_' + str(id) + '_hh',
                    TorchDummy())  # gates_matmal_hh
            setattr(self, 'resetgate_sigmoid_' + str(id),
                    TorchSigmoid())  # resetgate
            setattr(self, 'resetgate_add_' + str(id), TorchAdd())  # resetgate
            setattr(self, 'inputgate_sigmoid_' + str(id),
                    TorchSigmoid())  # inputgate
            setattr(self, 'inputgate_add_' + str(id), TorchAdd())  # inputgate
            setattr(self, 'newgate_tanh_' + str(id), TorchTanh())  # newgate
            setattr(self, 'newgate_add_' + str(id), TorchAdd())  # newgate
            setattr(self, 'newgate_dm_' + str(id), TorchDotMul())  # newgate
            setattr(self, 'hy_add_' + str(id), TorchAdd())  # hy
            setattr(self, 'hy_dm_' + str(id), TorchDotMul())  # hy
            setattr(self, 'hy_minus_' + str(id), TorchMinus())  # hy

    def gru_cell(self, id, input, hidden):
        """
        def gru_cell(input, hidden, w_ih, w_hh, b_ih, b_hh):
            gi = torch.mm(input, w_ih.t()) + b_ih
            gh = torch.mm(hidden, w_hh.t()) + b_hh
            i_r, i_i, i_n = gi.chunk(3, 1)
            h_r, h_i, h_n = gh.chunk(3, 1)

            resetgate = torch.sigmoid(i_r + h_r)
            inputgate = torch.sigmoid(i_i + h_i)
            newgate = torch.tanh(i_n + resetgate * h_n)
            hy = newgate + inputgate * (hidden - newgate)

            return hy
        """
        # get params
        w_ih = getattr(self, 'weight_ih_l' + str(id))
        w_hh = getattr(self, 'weight_hh_l' + str(id))
        b_ih = getattr(self, 'bias_ih_l' + str(id))
        b_hh = getattr(self, 'bias_hh_l' + str(id))

        # calculation
        hx = hidden
        gi = getattr(self, 'gates_mm_' + str(id) +
                     '_ih')(torch.mm(input, w_ih.t()) + b_ih)
        gh = getattr(self, 'gates_mm_' + str(id) +
                     '_hh')(torch.mm(hx, w_hh.t()) + b_hh)
        i_r, i_i, i_n = gi.chunk(3, 1)
        h_r, h_i, h_n = gi.chunk(3, 1)
        resetgate = getattr(self, 'resetgate_sigmoid_' + str(id))(getattr(
            self, 'resetgate_add_' + str(id))(i_r, h_r))
        inputgate = getattr(self, 'inputgate_sigmoid_' + str(id))(getattr(
            self, 'inputgate_add_' + str(id))(i_i, h_i))
        newgate = getattr(self, 'newgate_tanh_' + str(id))(getattr(
            self, 'newgate_add_' + str(id))(i_n,
                                            getattr(self, 'newgate_dm_' +
                                                    str(id)))(resetgate, h_n))
        hy = getattr(self, 'hy_add_' + str(id))(
            newgate, getattr(self, 'hy_dm_' + str(id))(
                inputgate, getattr(self, 'hy_minus_' + str(id)))(hidden,
                                                                 newgate))
        return hy

    def forward(self, input, hidden):
        #BUG fix forward code
        #TODO add PackedSequence support
        if self.batch_first:
            input = input.transpose(0, 1)
        result = []
        state = hidden
        hy, cy = hidden
        # https://stackoverflow.com/questions/62163194/pytorch-the-number-of-sizes-provided-0-must-be-greater-or-equal-to-the-number
        interh = []
        interc = []
        for t in input:
            interh = [x for x in hy]
            interc = [x for x in cy]
            for id in range(self.num_layers):
                in_t = t if id == 0 else interh[id - 1]
                interh[id], interc[id] = self.gru_cell(
                    id, in_t, (interh[id], interc[id]))
            result.append(interh[-1].data)
        result = torch.cat(result, 0)
        result = result.unsqueeze(1)
        state = (torch.cat([tensor.unsqueeze(0) for tensor in interh]),
                 torch.cat([tensor.unsqueeze(0) for tensor in interc]))
        return result, state


# REF: https://github.com/pytorch/pytorch/blob/master/benchmarks/fastrnns/cells.py
class QNQLSTM(nn.Module):
    def __init__(self,
                 input_size,
                 hidden_size,
                 num_layers,
                 bias: bool = True,
                 num_directions=1,
                 batch_first=False):

        super().__init__()
        self.batch_first = batch_first
        gate_size = 4 * hidden_size
        self.num_layers = num_layers
        self.num_directions = num_directions

        self.params = []

        for layer in range(num_layers):
            for direction in range(num_directions):
                layer_input_size = input_size if layer == 0 else hidden_size * num_directions

                w_ih = Parameter(torch.Tensor(gate_size, layer_input_size))
                w_hh = Parameter(torch.Tensor(gate_size, hidden_size))
                b_ih = Parameter(torch.Tensor(gate_size))
                # Second bias vector included for CuDNN compatibility. Only one
                # bias vector is needed in standard definition.
                b_hh = Parameter(torch.Tensor(gate_size))
                layer_params = (w_ih, w_hh, b_ih, b_hh)

                suffix = '_reverse' if direction == 1 else ''
                param_names = ['weight_ih_l{}{}', 'weight_hh_l{}{}']
                if bias:
                    param_names += ['bias_ih_l{}{}', 'bias_hh_l{}{}']
                param_names = [x.format(layer, suffix) for x in param_names]

                for name, param in zip(param_names, layer_params):
                    setattr(self, name, param)
                # add param_names in self.params for one line
                self.params.extend(param_names)

        # copy parameter to here
        for id in range(num_layers):
            setattr(self, 'gates_mm_' + str(id) + '_ih',
                    TorchDummy())  # gates_matmal_ih
            setattr(self, 'gates_mm_' + str(id) + '_hh',
                    TorchDummy())  # gates_matmal_hh
            setattr(self, 'gates_add_' + str(id), TorchDummy())  # gates_add_1
            setattr(self, 'ingate_sigmoid_' + str(id),
                    TorchSigmoid())  # ingate
            setattr(self, 'forgetgate_sigmoid_' + str(id),
                    TorchSigmoid())  # forgetgate
            setattr(self, 'cellgate_tanh_' + str(id), TorchTanh())  # cellgate
            setattr(self, 'outputgate_sigmoid_' + str(id),
                    TorchSigmoid())  # outgate
            setattr(self, 'cy_dm_' + str(id) + '_left', TorchDotMul())  # in cy
            setattr(self, 'cy_dm_' + str(id) + '_right',
                    TorchDotMul())  # in cy
            setattr(self, 'cy_add_' + str(id), TorchAdd())  # in cy
            setattr(self, 'hy_tanh_' + str(id), TorchTanh())  # in hy
            setattr(self, 'hy_dm_' + str(id), TorchDotMul())  # in hy

    def lstm_cell(self, id, input, hidden):
        # get params
        w_ih = getattr(self, 'weight_ih_l' + str(id))
        w_hh = getattr(self, 'weight_hh_l' + str(id))
        b_ih = getattr(self, 'bias_ih_l' + str(id))
        b_hh = getattr(self, 'bias_hh_l' + str(id))

        # calculation
        hx, cx = hidden
        a = getattr(self, 'gates_mm_' + str(id) +
                    '_ih')(torch.mm(input, w_ih.t()) + b_ih)
        b = getattr(self, 'gates_mm_' + str(id) +
                    '_hh')(torch.mm(hx, w_hh.t()) + b_hh)
        gates = getattr(self, 'gates_add_' + str(id))(a + b)
        ingate, forgetgate, cellgate, outgate = gates.chunk(4, 1)
        ingate = getattr(self, 'ingate_sigmoid_' + str(id))(ingate)
        forgetgate = getattr(self, 'forgetgate_sigmoid_' + str(id))(forgetgate)
        cellgate = getattr(self, 'cellgate_tanh_' + str(id))(cellgate)
        outgate = getattr(self, 'outputgate_sigmoid_' + str(id))(outgate)
        cy = getattr(self, 'cy_add_' + str(id))(
            getattr(self, 'cy_dm_' + str(id) + '_left')(forgetgate, cx),
            getattr(self, 'cy_dm_' + str(id) + '_right')(ingate, cellgate))
        hy = getattr(self,
                     'hy_dm_' + str(id))(outgate,
                                         getattr(self,
                                                 'hy_tanh_' + str(id))(cy))
        return hy, cy

    def forward(self, input, hidden):
        #TODO add PackedSequence support
        if self.batch_first:
            input = input.transpose(0, 1)
        result = []
        state = hidden
        hy, cy = hidden
        # https://stackoverflow.com/questions/62163194/pytorch-the-number-of-sizes-provided-0-must-be-greater-or-equal-to-the-number
        interh = []
        interc = []
        for t in input:
            interh = [x for x in hy]
            interc = [x for x in cy]
            for id in range(self.num_layers):
                in_t = t if id == 0 else interh[id - 1]
                interh[id], interc[id] = self.lstm_cell(
                    id, in_t, (interh[id], interc[id]))
            result.append(interh[-1].data)
        result = torch.cat(result, 0)
        result = result.unsqueeze(1)
        state = (torch.cat([tensor.unsqueeze(0) for tensor in interh]),
                 torch.cat([tensor.unsqueeze(0) for tensor in interc]))
        return result, state


class RNNBase(nn.Module):
    __constants__ = [
        'mode', 'input_size', 'hidden_size', 'num_layers', 'bias',
        'batch_first', 'dropout', 'bidirectional'
    ]

    def __init__(self,
                 mode: str,
                 input_size: int,
                 hidden_size: int,
                 num_layers: int = 1,
                 bias: bool = True,
                 batch_first: bool = False,
                 dropout: float = 0.,
                 bidirectional: bool = False) -> None:
        super(RNNBase, self).__init__()
        self.mode = mode
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.bias = bias
        self.batch_first = batch_first
        self.dropout = float(dropout)
        self.bidirectional = bidirectional
        num_directions = 2 if bidirectional else 1

        if not isinstance(dropout, numbers.Number) or not 0 <= dropout <= 1 or \
                isinstance(dropout, bool):
            raise ValueError(
                "dropout should be a number in range [0, 1] "
                "representing the probability of an element being "
                "zeroed")
        if dropout > 0 and num_layers == 1:
            warnings.warn("dropout option adds dropout after all but last "
                          "recurrent layer, so non-zero dropout expects "
                          "num_layers greater than 1, but got dropout={} and "
                          "num_layers={}".format(dropout, num_layers))

        if mode == 'LSTM':
            gate_size = 4 * hidden_size
        elif mode == 'GRU':
            gate_size = 3 * hidden_size
        elif mode == 'RNN_TANH':
            gate_size = hidden_size
        elif mode == 'RNN_RELU':
            gate_size = hidden_size
        else:
            raise ValueError("Unrecognized RNN mode: " + mode)

        self._flat_weights_names = []
        self._all_weights = []
        for layer in range(num_layers):
            for direction in range(num_directions):
                layer_input_size = input_size if layer == 0 else hidden_size * num_directions

                w_ih = Parameter(torch.Tensor(gate_size, layer_input_size))
                w_hh = Parameter(torch.Tensor(gate_size, hidden_size))
                b_ih = Parameter(torch.Tensor(gate_size))
                # Second bias vector included for CuDNN compatibility. Only one
                # bias vector is needed in standard definition.
                b_hh = Parameter(torch.Tensor(gate_size))
                layer_params = (w_ih, w_hh, b_ih, b_hh)

                suffix = '_reverse' if direction == 1 else ''
                param_names = ['weight_ih_l{}{}', 'weight_hh_l{}{}']
                if bias:
                    param_names += ['bias_ih_l{}{}', 'bias_hh_l{}{}']
                param_names = [x.format(layer, suffix) for x in param_names]

                for name, param in zip(param_names, layer_params):
                    setattr(self, name, param)
                self._flat_weights_names.extend(param_names)
                self._all_weights.append(param_names)

        self._flat_weights = [(lambda wn: getattr(self, wn)
                               if hasattr(self, wn) else None)(wn)
                              for wn in self._flat_weights_names]
        self.flatten_parameters()

    def __setattr__(self, attr, value):
        if hasattr(self,
                   "_flat_weights_names") and attr in self._flat_weights_names:
            # keep self._flat_weights up to date if you do self.weight = ...
            idx = self._flat_weights_names.index(attr)
            self._flat_weights[idx] = value
        super(RNNBase, self).__setattr__(attr, value)

    def flatten_parameters(self) -> None:
        """Resets parameter data pointer so that they can use faster code paths.

        Right now, this works only if the module is on the GPU and cuDNN is enabled.
        Otherwise, it's a no-op.
        """
        # Short-circuits if _flat_weights is only partially instantiated
        if len(self._flat_weights) != len(self._flat_weights_names):
            return

        for w in self._flat_weights:
            if not isinstance(w, Tensor):
                return
        # Short-circuits if any tensor in self._flat_weights is not acceptable to cuDNN
        # or the tensors in _flat_weights are of different dtypes

        first_fw = self._flat_weights[0]
        dtype = first_fw.dtype
        for fw in self._flat_weights:
            if (not isinstance(fw.data, Tensor) or not (fw.data.dtype == dtype)
                    or not fw.data.is_cuda
                    or not torch.backends.cudnn.is_acceptable(fw.data)):
                return

        # If any parameters alias, we fall back to the slower, copying code path. This is
        # a sufficient check, because overlapping parameter buffers that don't completely
        # alias would break the assumptions of the uniqueness check in
        # Module.named_parameters().
        unique_data_ptrs = set(p.data_ptr() for p in self._flat_weights)
        if len(unique_data_ptrs) != len(self._flat_weights):
            return

        with torch.cuda.device_of(first_fw):
            import torch.backends.cudnn.rnn as rnn

            # Note: no_grad() is necessary since _cudnn_rnn_flatten_weight is
            # an inplace operation on self._flat_weights
            with torch.no_grad():
                if torch._use_cudnn_rnn_flatten_weight():
                    torch._cudnn_rnn_flatten_weight(
                        self._flat_weights,
                        (4 if self.bias else 2), self.input_size,
                        rnn.get_cudnn_mode(self.mode), self.hidden_size,
                        self.num_layers, self.batch_first,
                        bool(self.bidirectional))

    def _apply(self, fn):
        ret = super(RNNBase, self)._apply(fn)

        # Resets _flat_weights
        # Note: be v. careful before removing this, as 3rd party device types
        # likely rely on this behavior to properly .to() modules like LSTM.
        self._flat_weights = [(lambda wn: getattr(self, wn)
                               if hasattr(self, wn) else None)(wn)
                              for wn in self._flat_weights_names]
        # Flattens params (on CUDA)
        self.flatten_parameters()

        return ret

    def check_input(self, input: Tensor,
                    batch_sizes: Optional[Tensor]) -> None:
        expected_input_dim = 2 if batch_sizes is not None else 3
        if input.dim() != expected_input_dim:
            raise RuntimeError('input must have {} dimensions, got {}'.format(
                expected_input_dim, input.dim()))
        if self.input_size != input.size(-1):
            raise RuntimeError(
                'input.size(-1) must be equal to input_size. Expected {}, got {}'
                .format(self.input_size, input.size(-1)))

    def get_expected_hidden_size(
            self, input: Tensor,
            batch_sizes: Optional[Tensor]) -> Tuple[int, int, int]:
        if batch_sizes is not None:
            mini_batch = batch_sizes[0]
            mini_batch = int(mini_batch)
        else:
            mini_batch = input.size(0) if self.batch_first else input.size(1)
        num_directions = 2 if self.bidirectional else 1
        expected_hidden_size = (self.num_layers * num_directions, mini_batch,
                                self.hidden_size)
        return expected_hidden_size

    def check_hidden_size(
            self,
            hx: Tensor,
            expected_hidden_size: Tuple[int, int, int],
            msg: str = 'Expected hidden size {}, got {}') -> None:
        if hx.size() != expected_hidden_size:
            raise RuntimeError(
                msg.format(expected_hidden_size, list(hx.size())))

    def check_forward_args(self, input: Tensor, hidden: Tensor,
                           batch_sizes: Optional[Tensor]):
        self.check_input(input, batch_sizes)
        expected_hidden_size = self.get_expected_hidden_size(
            input, batch_sizes)

        self.check_hidden_size(hidden, expected_hidden_size)

    def permute_hidden(self, hx: Tensor, permutation: Optional[Tensor]):
        if permutation is None:
            return hx
        return apply_permutation(hx, permutation)

    def forward(self,
                input: Tensor,
                hx: Optional[Tensor] = None) -> Tuple[Tensor, Tensor]:
        is_packed = isinstance(input, PackedSequence)
        if is_packed:
            input, batch_sizes, sorted_indices, unsorted_indices = input
            max_batch_size = batch_sizes[0]
            max_batch_size = int(max_batch_size)
        else:
            batch_sizes = None
            max_batch_size = input.size(0) if self.batch_first else input.size(
                1)
            sorted_indices = None
            unsorted_indices = None

        if hx is None:
            num_directions = 2 if self.bidirectional else 1
            hx = torch.zeros(self.num_layers * num_directions,
                             max_batch_size,
                             self.hidden_size,
                             dtype=input.dtype,
                             device=input.device)
        else:
            # Each batch of the hidden state should match the input sequence that
            # the user believes he/she is passing in.
            hx = self.permute_hidden(hx, sorted_indices)

        self.check_forward_args(input, hx, batch_sizes)
        #! del it
        result = [0, 1]
        if batch_sizes is None:
            #! need change
            pass
        else:
            #! need change
            pass
        output = result[0]
        hidden = result[1]

        if is_packed:
            output = PackedSequence(output, batch_sizes, sorted_indices,
                                    unsorted_indices)
        return output, self.permute_hidden(hidden, unsorted_indices)

    def extra_repr(self) -> str:
        s = '{input_size}, {hidden_size}'
        if self.num_layers != 1:
            s += ', num_layers={num_layers}'
        if self.bias is not True:
            s += ', bias={bias}'
        if self.batch_first is not False:
            s += ', batch_first={batch_first}'
        if self.dropout != 0:
            s += ', dropout={dropout}'
        if self.bidirectional is not False:
            s += ', bidirectional={bidirectional}'
        return s.format(**self.__dict__)

    def __setstate__(self, d):
        super(RNNBase, self).__setstate__(d)
        if 'all_weights' in d:
            self._all_weights = d['all_weights']

        if isinstance(self._all_weights[0][0], str):
            return
        num_layers = self.num_layers
        num_directions = 2 if self.bidirectional else 1
        self._flat_weights_names = []
        self._all_weights = []
        for layer in range(num_layers):
            for direction in range(num_directions):
                suffix = '_reverse' if direction == 1 else ''
                weights = [
                    'weight_ih_l{}{}', 'weight_hh_l{}{}', 'bias_ih_l{}{}',
                    'bias_hh_l{}{}'
                ]
                weights = [x.format(layer, suffix) for x in weights]
                if self.bias:
                    self._all_weights += [weights]
                    self._flat_weights_names.extend(weights)
                else:
                    self._all_weights += [weights[:2]]
                    self._flat_weights_names.extend(weights[:2])
        self._flat_weights = [(lambda wn: getattr(self, wn)
                               if hasattr(self, wn) else None)(wn)
                              for wn in self._flat_weights_names]

    @property
    def all_weights(self) -> List[Parameter]:
        return [[getattr(self, weight) for weight in weights]
                for weights in self._all_weights]

    def _replicate_for_data_parallel(self):
        replica = super(RNNBase, self)._replicate_for_data_parallel()
        # Need to copy these caches, otherwise the replica will share the same
        # flat weights list.
        replica._flat_weights = replica._flat_weights[:]
        replica._flat_weights_names = replica._flat_weights_names[:]
        return replica


class RNN(RNNBase):
    r"""Applies a multi-layer Elman RNN with :math:`\tanh` or :math:`\text{ReLU}` non-linearity to an
    input sequence.


    For each element in the input sequence, each layer computes the following
    function:

    .. math::
        h_t = \tanh(W_{ih} x_t + b_{ih} + W_{hh} h_{(t-1)} + b_{hh})

    where :math:`h_t` is the hidden state at time `t`, :math:`x_t` is
    the input at time `t`, and :math:`h_{(t-1)}` is the hidden state of the
    previous layer at time `t-1` or the initial hidden state at time `0`.
    If :attr:`nonlinearity` is ``'relu'``, then :math:`\text{ReLU}` is used instead of :math:`\tanh`.

    Args:
        input_size: The number of expected features in the input `x`
        hidden_size: The number of features in the hidden state `h`
        num_layers: Number of recurrent layers. E.g., setting ``num_layers=2``
            would mean stacking two RNNs together to form a `stacked RNN`,
            with the second RNN taking in outputs of the first RNN and
            computing the final results. Default: 1
        nonlinearity: The non-linearity to use. Can be either ``'tanh'`` or ``'relu'``. Default: ``'tanh'``
        bias: If ``False``, then the layer does not use bias weights `b_ih` and `b_hh`.
            Default: ``True``
        batch_first: If ``True``, then the input and output tensors are provided
            as `(batch, seq, feature)`. Default: ``False``
        dropout: If non-zero, introduces a `Dropout` layer on the outputs of each
            RNN layer except the last layer, with dropout probability equal to
            :attr:`dropout`. Default: 0
        bidirectional: If ``True``, becomes a bidirectional RNN. Default: ``False``

    Inputs: input, h_0
        - **input** of shape `(seq_len, batch, input_size)`: tensor containing the features
          of the input sequence. The input can also be a packed variable length
          sequence. See :func:`torch.nn.utils.rnn.pack_padded_sequence`
          or :func:`torch.nn.utils.rnn.pack_sequence`
          for details.
        - **h_0** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the initial hidden state for each element in the batch.
          Defaults to zero if not provided. If the RNN is bidirectional,
          num_directions should be 2, else it should be 1.

    Outputs: output, h_n
        - **output** of shape `(seq_len, batch, num_directions * hidden_size)`: tensor
          containing the output features (`h_t`) from the last layer of the RNN,
          for each `t`.  If a :class:`torch.nn.utils.rnn.PackedSequence` has
          been given as the input, the output will also be a packed sequence.

          For the unpacked case, the directions can be separated
          using ``output.view(seq_len, batch, num_directions, hidden_size)``,
          with forward and backward being direction `0` and `1` respectively.
          Similarly, the directions can be separated in the packed case.
        - **h_n** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the hidden state for `t = seq_len`.

          Like *output*, the layers can be separated using
          ``h_n.view(num_layers, num_directions, batch, hidden_size)``.

    Shape:
        - Input1: :math:`(L, N, H_{in})` tensor containing input features where
          :math:`H_{in}=\text{input\_size}` and `L` represents a sequence length.
        - Input2: :math:`(S, N, H_{out})` tensor
          containing the initial hidden state for each element in the batch.
          :math:`H_{out}=\text{hidden\_size}`
          Defaults to zero if not provided. where :math:`S=\text{num\_layers} * \text{num\_directions}`
          If the RNN is bidirectional, num_directions should be 2, else it should be 1.
        - Output1: :math:`(L, N, H_{all})` where :math:`H_{all}=\text{num\_directions} * \text{hidden\_size}`
        - Output2: :math:`(S, N, H_{out})` tensor containing the next hidden state
          for each element in the batch

    Attributes:
        weight_ih_l[k]: the learnable input-hidden weights of the k-th layer,
            of shape `(hidden_size, input_size)` for `k = 0`. Otherwise, the shape is
            `(hidden_size, num_directions * hidden_size)`
        weight_hh_l[k]: the learnable hidden-hidden weights of the k-th layer,
            of shape `(hidden_size, hidden_size)`
        bias_ih_l[k]: the learnable input-hidden bias of the k-th layer,
            of shape `(hidden_size)`
        bias_hh_l[k]: the learnable hidden-hidden bias of the k-th layer,
            of shape `(hidden_size)`

    .. note::
        All the weights and biases are initialized from :math:`\mathcal{U}(-\sqrt{k}, \sqrt{k})`
        where :math:`k = \frac{1}{\text{hidden\_size}}`

    .. include:: ../cudnn_rnn_determinism.rst

    .. include:: ../cudnn_persistent_rnn.rst

    Examples::

        >>> rnn = nn.RNN(10, 20, 2)
        >>> input = torch.randn(5, 3, 10)
        >>> h0 = torch.randn(2, 3, 20)
        >>> output, hn = rnn(input, h0)
    """
    def __init__(self, *args, **kwargs):
        self.nonlinearity = kwargs.pop('nonlinearity', 'tanh')
        if self.nonlinearity == 'tanh':
            mode = 'RNN_TANH'
        elif self.nonlinearity == 'relu':
            mode = 'RNN_RELU'
        else:
            raise ValueError("Unknown nonlinearity '{}'".format(
                self.nonlinearity))
        super(RNN, self).__init__(mode, *args, **kwargs)


# XXX: LSTM and GRU implementation is different from RNNBase, this is because:
# 1. we want to support nn.LSTM and nn.GRU in TorchScript and TorchScript in
#    its current state could not support the python Union Type or Any Type
# 2. TorchScript static typing does not allow a Function or Callable type in
#    Dict values, so we have to separately call _VF instead of using _rnn_impls
# 3. This is temporary only and in the transition state that we want to make it
#    on time for the release
#
# More discussion details in https://github.com/pytorch/pytorch/pull/23266
#
# TODO: remove the overriding implementations for LSTM and GRU when TorchScript
# support expressing these two modules generally.
class LSTM(RNNBase):
    r"""Applies a multi-layer long short-term memory (LSTM) RNN to an input
    sequence.


    For each element in the input sequence, each layer computes the following
    function:

    .. math::
        \begin{array}{ll} \\
            i_t = \sigma(W_{ii} x_t + b_{ii} + W_{hi} h_{t-1} + b_{hi}) \\
            f_t = \sigma(W_{if} x_t + b_{if} + W_{hf} h_{t-1} + b_{hf}) \\
            g_t = \tanh(W_{ig} x_t + b_{ig} + W_{hg} h_{t-1} + b_{hg}) \\
            o_t = \sigma(W_{io} x_t + b_{io} + W_{ho} h_{t-1} + b_{ho}) \\
            c_t = f_t \odot c_{t-1} + i_t \odot g_t \\
            h_t = o_t \odot \tanh(c_t) \\
        \end{array}

    where :math:`h_t` is the hidden state at time `t`, :math:`c_t` is the cell
    state at time `t`, :math:`x_t` is the input at time `t`, :math:`h_{t-1}`
    is the hidden state of the layer at time `t-1` or the initial hidden
    state at time `0`, and :math:`i_t`, :math:`f_t`, :math:`g_t`,
    :math:`o_t` are the input, forget, cell, and output gates, respectively.
    :math:`\sigma` is the sigmoid function, and :math:`\odot` is the Hadamard product.

    In a multilayer LSTM, the input :math:`x^{(l)}_t` of the :math:`l` -th layer
    (:math:`l >= 2`) is the hidden state :math:`h^{(l-1)}_t` of the previous layer multiplied by
    dropout :math:`\delta^{(l-1)}_t` where each :math:`\delta^{(l-1)}_t` is a Bernoulli random
    variable which is :math:`0` with probability :attr:`dropout`.

    Args:
        input_size: The number of expected features in the input `x`
        hidden_size: The number of features in the hidden state `h`
        num_layers: Number of recurrent layers. E.g., setting ``num_layers=2``
            would mean stacking two LSTMs together to form a `stacked LSTM`,
            with the second LSTM taking in outputs of the first LSTM and
            computing the final results. Default: 1
        bias: If ``False``, then the layer does not use bias weights `b_ih` and `b_hh`.
            Default: ``True``
        batch_first: If ``True``, then the input and output tensors are provided
            as (batch, seq, feature). Default: ``False``
        dropout: If non-zero, introduces a `Dropout` layer on the outputs of each
            LSTM layer except the last layer, with dropout probability equal to
            :attr:`dropout`. Default: 0
        bidirectional: If ``True``, becomes a bidirectional LSTM. Default: ``False``

    Inputs: input, (h_0, c_0)
        - **input** of shape `(seq_len, batch, input_size)`: tensor containing the features
          of the input sequence.
          The input can also be a packed variable length sequence.
          See :func:`torch.nn.utils.rnn.pack_padded_sequence` or
          :func:`torch.nn.utils.rnn.pack_sequence` for details.
        - **h_0** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the initial hidden state for each element in the batch.
          If the LSTM is bidirectional, num_directions should be 2, else it should be 1.
        - **c_0** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the initial cell state for each element in the batch.

          If `(h_0, c_0)` is not provided, both **h_0** and **c_0** default to zero.


    Outputs: output, (h_n, c_n)
        - **output** of shape `(seq_len, batch, num_directions * hidden_size)`: tensor
          containing the output features `(h_t)` from the last layer of the LSTM,
          for each `t`. If a :class:`torch.nn.utils.rnn.PackedSequence` has been
          given as the input, the output will also be a packed sequence.

          For the unpacked case, the directions can be separated
          using ``output.view(seq_len, batch, num_directions, hidden_size)``,
          with forward and backward being direction `0` and `1` respectively.
          Similarly, the directions can be separated in the packed case.
        - **h_n** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the hidden state for `t = seq_len`.

          Like *output*, the layers can be separated using
          ``h_n.view(num_layers, num_directions, batch, hidden_size)`` and similarly for *c_n*.
        - **c_n** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the cell state for `t = seq_len`.

    Attributes:
        weight_ih_l[k] : the learnable input-hidden weights of the :math:`\text{k}^{th}` layer
            `(W_ii|W_if|W_ig|W_io)`, of shape `(4*hidden_size, input_size)` for `k = 0`.
            Otherwise, the shape is `(4*hidden_size, num_directions * hidden_size)`
        weight_hh_l[k] : the learnable hidden-hidden weights of the :math:`\text{k}^{th}` layer
            `(W_hi|W_hf|W_hg|W_ho)`, of shape `(4*hidden_size, hidden_size)`
        bias_ih_l[k] : the learnable input-hidden bias of the :math:`\text{k}^{th}` layer
            `(b_ii|b_if|b_ig|b_io)`, of shape `(4*hidden_size)`
        bias_hh_l[k] : the learnable hidden-hidden bias of the :math:`\text{k}^{th}` layer
            `(b_hi|b_hf|b_hg|b_ho)`, of shape `(4*hidden_size)`

    .. note::
        All the weights and biases are initialized from :math:`\mathcal{U}(-\sqrt{k}, \sqrt{k})`
        where :math:`k = \frac{1}{\text{hidden\_size}}`

    .. include:: ../cudnn_rnn_determinism.rst

    .. include:: ../cudnn_persistent_rnn.rst

    Examples::

        >>> rnn = nn.LSTM(10, 20, 2)
        >>> input = torch.randn(5, 3, 10)
        >>> h0 = torch.randn(2, 3, 20)
        >>> c0 = torch.randn(2, 3, 20)
        >>> output, (hn, cn) = rnn(input, (h0, c0))
    """
    def __init__(self, *args, **kwargs):
        super(LSTM, self).__init__('LSTM', *args, **kwargs)

    def check_forward_args(self, input: Tensor, hidden: Tuple[Tensor, Tensor],
                           batch_sizes: Optional[Tensor]):
        self.check_input(input, batch_sizes)
        expected_hidden_size = self.get_expected_hidden_size(
            input, batch_sizes)

        self.check_hidden_size(hidden[0], expected_hidden_size,
                               'Expected hidden[0] size {}, got {}')
        self.check_hidden_size(hidden[1], expected_hidden_size,
                               'Expected hidden[1] size {}, got {}')

    def permute_hidden(self, hx: Tuple[Tensor, Tensor],
                       permutation: Optional[Tensor]) -> Tuple[Tensor, Tensor]:
        if permutation is None:
            return hx
        return apply_permutation(hx[0], permutation), apply_permutation(
            hx[1], permutation)

    @overload
    @torch._jit_internal._overload_method  # noqa: F811
    def forward(
        self,
        input: Tensor,
        hx: Optional[Tuple[Tensor, Tensor]] = None
    ) -> Tuple[Tensor, Tuple[Tensor, Tensor]]:  # noqa: F811
        pass

    @overload
    @torch._jit_internal._overload_method  # noqa: F811
    def forward(
        self,
        input: PackedSequence,
        hx: Optional[Tuple[Tensor, Tensor]] = None
    ) -> Tuple[PackedSequence, Tuple[Tensor, Tensor]]:  # noqa: F811
        pass

    def forward(self, input, hx=None):  # noqa: F811
        orig_input = input
        # xxx: isinstance check needs to be in conditional for TorchScript to compile
        if isinstance(orig_input, PackedSequence):
            input, batch_sizes, sorted_indices, unsorted_indices = input
            max_batch_size = batch_sizes[0]
            max_batch_size = int(max_batch_size)
        else:
            batch_sizes = None
            max_batch_size = input.size(0) if self.batch_first else input.size(
                1)
            sorted_indices = None
            unsorted_indices = None

        if hx is None:
            num_directions = 2 if self.bidirectional else 1
            zeros = torch.zeros(self.num_layers * num_directions,
                                max_batch_size,
                                self.hidden_size,
                                dtype=input.dtype,
                                device=input.device)
            hx = (zeros, zeros)
        else:
            # Each batch of the hidden state should match the input sequence that
            # the user believes he/she is passing in.
            hx = self.permute_hidden(hx, sorted_indices)

        self.check_forward_args(input, hx, batch_sizes)
        #! del it
        result = [0, 1]
        if batch_sizes is None:
            #! need change
            pass
        else:
            #! need change
            pass
        output = result[0]
        hidden = result[1:]
        # xxx: isinstance check needs to be in conditional for TorchScript to compile
        if isinstance(orig_input, PackedSequence):
            output_packed = PackedSequence(output, batch_sizes, sorted_indices,
                                           unsorted_indices)
            return output_packed, self.permute_hidden(hidden, unsorted_indices)
        else:
            return output, self.permute_hidden(hidden, unsorted_indices)


class GRU(RNNBase):
    r"""Applies a multi-layer gated recurrent unit (GRU) RNN to an input sequence.


    For each element in the input sequence, each layer computes the following
    function:

    .. math::
        \begin{array}{ll}
            r_t = \sigma(W_{ir} x_t + b_{ir} + W_{hr} h_{(t-1)} + b_{hr}) \\
            z_t = \sigma(W_{iz} x_t + b_{iz} + W_{hz} h_{(t-1)} + b_{hz}) \\
            n_t = \tanh(W_{in} x_t + b_{in} + r_t * (W_{hn} h_{(t-1)}+ b_{hn})) \\
            h_t = (1 - z_t) * n_t + z_t * h_{(t-1)}
        \end{array}

    where :math:`h_t` is the hidden state at time `t`, :math:`x_t` is the input
    at time `t`, :math:`h_{(t-1)}` is the hidden state of the layer
    at time `t-1` or the initial hidden state at time `0`, and :math:`r_t`,
    :math:`z_t`, :math:`n_t` are the reset, update, and new gates, respectively.
    :math:`\sigma` is the sigmoid function, and :math:`*` is the Hadamard product.

    In a multilayer GRU, the input :math:`x^{(l)}_t` of the :math:`l` -th layer
    (:math:`l >= 2`) is the hidden state :math:`h^{(l-1)}_t` of the previous layer multiplied by
    dropout :math:`\delta^{(l-1)}_t` where each :math:`\delta^{(l-1)}_t` is a Bernoulli random
    variable which is :math:`0` with probability :attr:`dropout`.

    Args:
        input_size: The number of expected features in the input `x`
        hidden_size: The number of features in the hidden state `h`
        num_layers: Number of recurrent layers. E.g., setting ``num_layers=2``
            would mean stacking two GRUs together to form a `stacked GRU`,
            with the second GRU taking in outputs of the first GRU and
            computing the final results. Default: 1
        bias: If ``False``, then the layer does not use bias weights `b_ih` and `b_hh`.
            Default: ``True``
        batch_first: If ``True``, then the input and output tensors are provided
            as (batch, seq, feature). Default: ``False``
        dropout: If non-zero, introduces a `Dropout` layer on the outputs of each
            GRU layer except the last layer, with dropout probability equal to
            :attr:`dropout`. Default: 0
        bidirectional: If ``True``, becomes a bidirectional GRU. Default: ``False``

    Inputs: input, h_0
        - **input** of shape `(seq_len, batch, input_size)`: tensor containing the features
          of the input sequence. The input can also be a packed variable length
          sequence. See :func:`torch.nn.utils.rnn.pack_padded_sequence`
          for details.
        - **h_0** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the initial hidden state for each element in the batch.
          Defaults to zero if not provided. If the RNN is bidirectional,
          num_directions should be 2, else it should be 1.

    Outputs: output, h_n
        - **output** of shape `(seq_len, batch, num_directions * hidden_size)`: tensor
          containing the output features h_t from the last layer of the GRU,
          for each `t`. If a :class:`torch.nn.utils.rnn.PackedSequence` has been
          given as the input, the output will also be a packed sequence.
          For the unpacked case, the directions can be separated
          using ``output.view(seq_len, batch, num_directions, hidden_size)``,
          with forward and backward being direction `0` and `1` respectively.

          Similarly, the directions can be separated in the packed case.
        - **h_n** of shape `(num_layers * num_directions, batch, hidden_size)`: tensor
          containing the hidden state for `t = seq_len`

          Like *output*, the layers can be separated using
          ``h_n.view(num_layers, num_directions, batch, hidden_size)``.

    Shape:
        - Input1: :math:`(L, N, H_{in})` tensor containing input features where
          :math:`H_{in}=\text{input\_size}` and `L` represents a sequence length.
        - Input2: :math:`(S, N, H_{out})` tensor
          containing the initial hidden state for each element in the batch.
          :math:`H_{out}=\text{hidden\_size}`
          Defaults to zero if not provided. where :math:`S=\text{num\_layers} * \text{num\_directions}`
          If the RNN is bidirectional, num_directions should be 2, else it should be 1.
        - Output1: :math:`(L, N, H_{all})` where :math:`H_{all}=\text{num\_directions} * \text{hidden\_size}`
        - Output2: :math:`(S, N, H_{out})` tensor containing the next hidden state
          for each element in the batch

    Attributes:
        weight_ih_l[k] : the learnable input-hidden weights of the :math:`\text{k}^{th}` layer
            (W_ir|W_iz|W_in), of shape `(3*hidden_size, input_size)` for `k = 0`.
            Otherwise, the shape is `(3*hidden_size, num_directions * hidden_size)`
        weight_hh_l[k] : the learnable hidden-hidden weights of the :math:`\text{k}^{th}` layer
            (W_hr|W_hz|W_hn), of shape `(3*hidden_size, hidden_size)`
        bias_ih_l[k] : the learnable input-hidden bias of the :math:`\text{k}^{th}` layer
            (b_ir|b_iz|b_in), of shape `(3*hidden_size)`
        bias_hh_l[k] : the learnable hidden-hidden bias of the :math:`\text{k}^{th}` layer
            (b_hr|b_hz|b_hn), of shape `(3*hidden_size)`

    .. note::
        All the weights and biases are initialized from :math:`\mathcal{U}(-\sqrt{k}, \sqrt{k})`
        where :math:`k = \frac{1}{\text{hidden\_size}}`

    .. include:: ../cudnn_persistent_rnn.rst

    Examples::

        >>> rnn = nn.GRU(10, 20, 2)
        >>> input = torch.randn(5, 3, 10)
        >>> h0 = torch.randn(2, 3, 20)
        >>> output, hn = rnn(input, h0)
    """
    def __init__(self, *args, **kwargs):
        super(GRU, self).__init__('GRU', *args, **kwargs)
        #! add by dongz

    @overload
    @torch._jit_internal._overload_method  # noqa: F811
    def forward(
            self,
            input: Tensor,
            hx: Optional[Tensor] = None
    ) -> Tuple[Tensor, Tensor]:  # noqa: F811
        pass

    @overload
    @torch._jit_internal._overload_method  # noqa: F811
    def forward(
        self,
        input: PackedSequence,
        hx: Optional[Tensor] = None
    ) -> Tuple[PackedSequence, Tensor]:  # noqa: F811
        pass

    def forward(self, input, hx=None):  # noqa: F811
        orig_input = input
        # xxx: isinstance check needs to be in conditional for TorchScript to compile
        if isinstance(orig_input, PackedSequence):
            input, batch_sizes, sorted_indices, unsorted_indices = input
            max_batch_size = batch_sizes[0]
            max_batch_size = int(max_batch_size)
        else:
            batch_sizes = None
            max_batch_size = input.size(0) if self.batch_first else input.size(
                1)
            sorted_indices = None
            unsorted_indices = None

        if hx is None:
            num_directions = 2 if self.bidirectional else 1
            hx = torch.zeros(self.num_layers * num_directions,
                             max_batch_size,
                             self.hidden_size,
                             dtype=input.dtype,
                             device=input.device)
        else:
            # Each batch of the hidden state should match the input sequence that
            # the user believes he/she is passing in.
            hx = self.permute_hidden(hx, sorted_indices)

        self.check_forward_args(input, hx, batch_sizes)
        #! edit by dongz
        if batch_sizes is None:
            pass
        else:
            pass
        output = result[0]
        hidden = result[1]

        # xxx: isinstance check needs to be in conditional for TorchScript to compile
        if isinstance(orig_input, PackedSequence):
            output_packed = PackedSequence(output, batch_sizes, sorted_indices,
                                           unsorted_indices)
            return output_packed, self.permute_hidden(hidden, unsorted_indices)
        else:
            return output, self.permute_hidden(hidden, unsorted_indices)
