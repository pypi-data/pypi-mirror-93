"""
Tests for the quantnn.quantiles module.
"""
import einops as eo
import numpy as np
import pytest
from quantnn.generic import sample_uniform, to_array, arange, reshape
from quantnn.quantiles import (cdf, pdf, pdf_binned, posterior_mean, crps,
                               probability_less_than,
                               probability_larger_than,
                               sample_posterior,
                               sample_posterior_gaussian,
                               quantile_loss)

@pytest.mark.parametrize("xp", pytest.backends)
def test_cdf(xp):
    """
    Tests the calculation of the pdf for different shapes of input
    arrays.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    x_cdf, y_cdf = cdf(y_pred, quantiles)
    assert np.all(np.isclose(x_cdf[0], -xp.ones_like(x_cdf[0])))
    assert np.all(np.isclose(x_cdf[-1], 11.0 * xp.ones_like(x_cdf[-1])))

    #
    # 2D predictions
    #

    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    x_cdf, y_cdf = cdf(y_pred, quantiles)
    assert np.all(np.isclose(x_cdf[:, 0], -xp.ones_like(x_cdf[:, 0])))
    assert np.all(np.isclose(x_cdf[:, -1], 11.0 * xp.ones_like(x_cdf[:, -1])))

    #
    # 3D predictions, quantiles along last axis
    #

    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    x_cdf, y_cdf = cdf(y_pred, quantiles, quantile_axis=-1)
    assert np.all(np.isclose(x_cdf[:, :, 0], -xp.ones_like(x_cdf[:, :, 0])))
    assert np.all(np.isclose(x_cdf[:, :, -1], 11.0 * xp.ones_like(x_cdf[:, :, -1])))

    #
    # 3D predictions, quantiles along first axis
    #

    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', h=10, w=10)
    x_cdf, y_cdf = cdf(y_pred, quantiles, quantile_axis=1)
    assert np.all(np.isclose(x_cdf[:, 0, :], -xp.ones_like(x_cdf[:, 0, :])))
    assert np.all(np.isclose(x_cdf[:, -1, :], 11.0 * xp.ones_like(x_cdf[:, -1, :])))

@pytest.mark.parametrize("xp", pytest.backends)
def test_pdf(xp):
    """
    Tests the calculation of the pdf for different shapes of input
    arrays.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    x_pdf, y_pdf = pdf(y_pred, quantiles)
    assert np.all(np.isclose(x_pdf[2:-2], arange(xp, 1.5, 8.6, 1.0)))
    assert np.all(np.isclose(y_pdf[0], xp.zeros_like(y_pdf[0])))
    assert np.all(np.isclose(y_pdf[-1], xp.zeros_like(y_pdf[-1])))
    assert np.all(np.isclose(y_pdf[2:-2], 0.1 * xp.ones_like(y_pdf[2:-2])))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    x_pdf, y_pdf = pdf(y_pred, quantiles)
    assert np.all(np.isclose(x_pdf[:, 2:-2],
                             reshape(xp, arange(xp, 1.5, 8.6, 1.0), (1, -1))))
    assert np.all(np.isclose(y_pdf[:, 0], xp.zeros_like(y_pdf[:, 0])))
    assert np.all(np.isclose(y_pdf[:, -1], xp.zeros_like(y_pdf[:, -1])))
    assert np.all(np.isclose(y_pdf[:, 2:-2], 0.1 * xp.ones_like(y_pdf[:, 2:-2])))

    #
    # 3D predictions, quantiles along last axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    x_pdf, y_pdf = pdf(y_pred, quantiles, quantile_axis=-1)
    assert np.all(np.isclose(x_pdf[:, :, 2:-2],
                             reshape(xp, arange(xp, 1.5, 8.6, 1.0), (1, 1, -1))))
    assert np.all(np.isclose(y_pdf[:, :, 0], xp.zeros_like(y_pdf[:, :, 0])))
    assert np.all(np.isclose(y_pdf[:, :, -1], xp.zeros_like(y_pdf[:, :, -1])))
    assert np.all(np.isclose(y_pdf[:, :, 2:-2], 0.1 * xp.ones_like(y_pdf[:, :, 2:-2])))

    #
    # 3D predictions, quantiles along first axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', h=10, w=10)
    x_pdf, y_pdf = pdf(y_pred, quantiles, quantile_axis=1)
    assert np.all(np.isclose(x_pdf[:, 2:-2, :],
                             reshape(xp, arange(xp, 1.5, 8.6, 1.0), (1, -1, 1))))
    assert np.all(np.isclose(y_pdf[:, 0, :], xp.zeros_like(y_pdf[:, 0, :])))
    assert np.all(np.isclose(y_pdf[:, -1, :], xp.zeros_like(y_pdf[:, -1, :])))
    assert np.all(np.isclose(y_pdf[:, 2:-2, :], 0.1 * xp.ones_like(y_pdf[:, 2:-2, :])))

@pytest.mark.parametrize("xp", pytest.backends)
def test_pdf_binned(xp):
    """
    Tests the calculation of the pdf for different shapes of input
    arrays.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    bins = arange(xp, 1.0, 9.01, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins)
    assert np.all(np.isclose(y_pdf_binned, 0.1, 1e-3))

    # Test extrapolation left
    bins = arange(xp, -2.0, -1.0, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins)
    assert np.all(np.isclose(y_pdf_binned, 0.0, 1e-3))

    # Test extrapolation right
    bins = arange(xp, 11.1, 12.0, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins)
    assert np.all(np.isclose(y_pdf_binned, 0.0, 1e-3))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    bins = arange(xp, 1.0, 9.01, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins)
    assert np.all(np.isclose(y_pdf_binned, 0.1, 1e-3))

    # Test extrapolation left
    bins = arange(xp, -2.0, -1.0, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins)
    assert np.all(np.isclose(y_pdf_binned, 0.0, 1e-3))

    # Test extrapolation right
    bins = arange(xp, 11.1, 12.0, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins)
    assert np.all(np.isclose(y_pdf_binned, 0.0, 1e-3))

    #
    # 3D predictions, quantiles along last axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    bins = arange(xp, 1.0, 9.01, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins, quantile_axis=-1)
    assert np.all(np.isclose(y_pdf_binned, 0.1, 1e-3))

    # Test extrapolation left
    bins = arange(xp, -2.0, -1.0, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins, quantile_axis=-1)
    assert np.all(np.isclose(y_pdf_binned, 0.0, 1e-3))

    # Test extrapolation right
    bins = arange(xp, 11.1, 12.0, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins, quantile_axis=-1)
    assert np.all(np.isclose(y_pdf_binned, 0.0, 1e-3))

    #
    # 3D predictions, quantiles along first axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> q h w', h=10, w=10)
    bins = arange(xp, 1.0, 9.01, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins, quantile_axis=0)
    assert np.all(np.isclose(y_pdf_binned, 0.1, 1e-3))

    # Test extrapolation left
    bins = arange(xp, -2.0, -1.0, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins, quantile_axis=0)
    assert np.all(np.isclose(y_pdf_binned, 0.0, 1e-3))

    # Test extrapolation right
    bins = arange(xp, 11.1, 12.0, 0.1)
    y_pdf_binned = pdf_binned(y_pred, quantiles, bins, quantile_axis=0)
    assert np.all(np.isclose(y_pdf_binned, 0.0, 1e-3))

@pytest.mark.parametrize("xp", pytest.backends)
def test_posterior_mean(xp):
    """
    Tests the calculation of the posterior mean for different shapes of
    input arrays.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    means = posterior_mean(y_pred, quantiles)
    assert np.all(np.isclose(means, 5.0 * xp.ones_like(means)))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    means = posterior_mean(y_pred, quantiles)
    assert np.all(np.isclose(means, 5.0 * xp.ones_like(means)))

    #
    # 3D predictions, quantiles along last axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    means = posterior_mean(y_pred, quantiles, quantile_axis=-1)
    assert np.all(np.isclose(means, 5.0 * xp.ones_like(means)))

    #
    # 3D predictions, quantiles along first axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', h=10, w=10)
    means = posterior_mean(y_pred, quantiles, quantile_axis=1)
    assert np.all(np.isclose(means, 5.0 * xp.ones_like(means)))

@pytest.mark.parametrize("xp", pytest.backends)
def test_crps(xp):
    """
    Tests the calculation of the CRPS for different shapes of input
    arrays.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    scores = crps(y_pred, quantiles, 4.9)
    assert np.all(np.isclose(scores, 0.86 * xp.ones_like(scores)))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    y_true = 4.9 * xp.ones(10)
    scores = crps(y_pred, quantiles, y_true)
    assert np.all(np.isclose(scores, 0.86 * xp.ones_like(scores)))

    ##
    ## 3D predictions, quantiles along last axis
    ##

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', w=10, h=10)
    y_true = 4.9 * xp.ones((10, 10))
    scores = crps(y_pred, quantiles, y_true, quantile_axis=2)
    assert np.all(np.isclose(scores, 0.86 * xp.ones_like(scores)))

    ##
    ## 3D predictions, quantiles along first axis
    ##

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', w=10, h=10)
    y_true = 4.9 * xp.ones((10, 10))
    scores = crps(y_pred, quantiles, y_true, quantile_axis=1)
    assert np.all(np.isclose(scores, 0.86 * xp.ones_like(scores)))

@pytest.mark.parametrize("xp", pytest.backends)
def test_probability_less_than(xp):
    """
    Tests predicting the probability that the true value is lower
    than a given threshold.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    t = 1.0 + 8.0 * np.random.rand()
    probability = probability_less_than(y_pred, quantiles, t)
    assert np.all(np.isclose(probability, 0.1 * t * xp.ones_like(probability)))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    t = 1.0 + 8.0 * np.random.rand()
    probability = probability_less_than(y_pred, quantiles, t)
    assert np.all(np.isclose(probability, 0.1 * t * xp.ones_like(probability)))

    #
    # 3D predictions, quantiles along last axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    t = 1.0 + 8.0 * np.random.rand()
    probability = probability_less_than(y_pred, quantiles, t, quantile_axis=2)
    assert np.all(np.isclose(probability, 0.1 * t * xp.ones_like(probability)))

    #
    # 3D predictions, quantiles along first axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', h=10, w=10)
    t = 1.0 + 8.0 * np.random.rand()
    probability = probability_less_than(y_pred, quantiles, t, quantile_axis=1)
    assert np.all(np.isclose(probability, 0.1 * t * xp.ones_like(probability)))

@pytest.mark.parametrize("xp", pytest.backends)
def test_probability_larger_than(xp):
    """
    Tests predicting the probability that the true value is larger
    than a given threshold.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    t = 1.0 + 8.0 * np.random.rand()
    probability = probability_larger_than(y_pred, quantiles, t)
    assert np.all(np.isclose(probability, 1.0 - 0.1 * t * xp.ones_like(probability)))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    t = 1.0 + 8.0 * np.random.rand()
    probability = probability_larger_than(y_pred, quantiles, t)
    assert np.all(np.isclose(probability, 1.0 - 0.1 * t * xp.ones_like(probability)))

    #
    # 3D predictions, quantiles along last axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    t = 1.0 + 8.0 * np.random.rand()
    probability = probability_larger_than(y_pred, quantiles, t, quantile_axis=2)
    assert np.all(np.isclose(probability, 1.0 - 0.1 * t * xp.ones_like(probability)))

    #
    # 3D predictions, quantiles along first axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', h=10, w=10)
    t = 1.0 + 8.0 * np.random.rand()
    probability = probability_larger_than(y_pred, quantiles, t, quantile_axis=1)
    assert np.all(np.isclose(probability, 1.0 - 0.1 * t * xp.ones_like(probability)))

@pytest.mark.parametrize("xp", pytest.backends)
def test_sample_posterior(xp):
    """
    Tests sampling from the posterior by interpolation of inverse CDF.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    samples = sample_posterior(y_pred, quantiles, n_samples=10000)
    assert np.all(np.isclose(samples.mean(),
                             5.0 * xp.ones_like(samples.mean()),
                             1e-1))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    samples = sample_posterior(y_pred, quantiles, n_samples=10000)
    assert np.all(np.isclose(samples.mean(),
                             5.0 * xp.ones_like(samples.mean()),
                             1e-1))

    #
    # 3D predictions, quantiles along last axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    samples = sample_posterior(y_pred, quantiles, n_samples=1000,
                               quantile_axis=2)
    assert np.all(np.isclose(samples.mean(),
                             5.0 * xp.ones_like(samples.mean()),
                             1e-1))

    #
    # 3D predictions, quantiles along first axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', h=10, w=10)
    samples = sample_posterior(y_pred, quantiles, n_samples=1000,
                               quantile_axis=1)
    assert np.all(np.isclose(samples.mean(),
                             5.0 * xp.ones_like(samples.mean()),
                             1e-1))

@pytest.mark.parametrize("xp", pytest.backends)
def test_sample_posterior_gaussian(xp):
    """
    Tests sampling from the posterior by fitting a Gaussian.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    samples = sample_posterior_gaussian(y_pred, quantiles, n_samples=10000)
    assert np.all(np.isclose(samples.mean(),
                             5.0 * xp.ones_like(samples.mean()),
                             1e-1))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    samples = sample_posterior_gaussian(y_pred, quantiles, n_samples=10000)
    assert np.all(np.isclose(samples.mean(),
                             5.0 * xp.ones_like(samples.mean()),
                             1e-1))

    #
    # 3D predictions, quantiles along last axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    samples = sample_posterior_gaussian(y_pred, quantiles, n_samples=1000,
                               quantile_axis=2)
    assert np.all(np.isclose(samples.mean(),
                             5.0 * xp.ones_like(samples.mean()),
                             1e-1))

    #
    # 3D predictions, quantiles along first axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', h=10, w=10)
    samples = sample_posterior_gaussian(y_pred, quantiles, n_samples=1000,
                               quantile_axis=1)
    assert np.all(np.isclose(samples.mean(),
                             5.0 * xp.ones_like(samples.mean()),
                             1e-1))

@pytest.mark.parametrize("xp", pytest.backends)
def test_quantile_loss(xp):
    """
    Tests calculation of the quantile loss function.
    """

    #
    # 1D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = arange(xp, 1.0, 9.1, 1.0)
    y_true = to_array(xp, [5.0])
    loss = quantile_loss(y_pred, quantiles, y_true)
    assert np.isclose(loss.mean(), to_array(xp, [0.444444]))

    #
    # 2D predictions
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> w q', w=10)
    y_true = eo.repeat(to_array(xp, [5.0]), 'q -> w q', w=10)
    loss = quantile_loss(y_pred, quantiles, y_true)
    assert np.isclose(loss.mean(), to_array(xp, [0.444444]))

    #
    # 3D predictions, quantiles along last axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h w q', h=10, w=10)
    y_true = eo.repeat(to_array(xp, [5.0]), 'q -> h w q', h=10, w=10)
    loss = quantile_loss(y_pred, quantiles,  y_true, quantile_axis=-1)
    assert np.isclose(loss.mean(), to_array(xp, [0.444444]))

    #
    # 3D predictions, quantiles along first axis
    #

    quantiles = arange(xp, 0.1, 0.91, 0.1)
    y_pred = eo.repeat(arange(xp, 1.0, 9.1, 1.0), 'q -> h q w', h=10, w=10)
    y_true = eo.repeat(to_array(xp, [5.0]), 'q -> h q w', h=10, w=10)
    loss = quantile_loss(y_pred, quantiles, y_true, quantile_axis=1)
    assert np.isclose(loss.mean(), to_array(xp, [0.444444]))
