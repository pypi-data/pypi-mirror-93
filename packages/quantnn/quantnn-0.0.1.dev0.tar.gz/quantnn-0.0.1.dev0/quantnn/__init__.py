"""
=======
quantnn
=======

The quantnn package provides functionality for probabilistic modeling and prediction
using deep neural networks.

The two main features of the quantnn package are implemented by the
:py:class:`~quantnn.qrnn.QRNN` and :py:class:`~quantnn.qrnn.DRNN` classes, which implement
quantile regression neural networks (QRNNs) and density regression neural networks (DRNNs),
respectively.

The modules :py:mod:`quantnn.quantiles` and :py:mod:`quantnn.density` provide generic
(backend agnostic) functions to manipulate probabilistic predictions.
"""
from quantnn.neural_network_model import (set_default_backend,
                                          get_default_backend)
from quantnn.qrnn import QRNN
from quantnn.drnn import DRNN
from quantnn.quantiles import (cdf,
                               pdf,
                               posterior_mean,
                               probability_less_than,
                               probability_larger_than,
                               sample_posterior,
                               sample_posterior_gaussian,
                               quantile_loss)
