"""
Tests for generic array manipulation functions.
"""
import numpy as np
import pytest
from quantnn.generic import (get_array_module,
                             to_array,
                             sample_uniform,
                             sample_gaussian,
                             numel,
                             concatenate,
                             expand_dims,
                             pad_zeros,
                             pad_zeros_left,
                             as_type,
                             arange,
                             reshape,
                             trapz,
                             cumsum,
                             cumtrapz)

@pytest.mark.parametrize("backend", pytest.backends)
def test_get_array_module(backend):
    """
    Ensures that get_array_module returns right array object
    when given an array created using the arange method of the
    corresponding module object.
    """
    x = backend.ones(10)
    module = get_array_module(x)
    assert module == backend

@pytest.mark.parametrize("backend", pytest.backends)
def test_to_array(backend):
    """
    Converts numpy array to array of given backend and ensures
    that corresponding module object matches the backend.
    """
    x = np.arange(10)
    array = to_array(backend, x)
    assert get_array_module(array) == backend

@pytest.mark.parametrize("backend", pytest.backends)
def test_sample_uniform(backend):
    """
    Ensures that array of random samples has array type
    corresponding to the right backend module.
    """
    samples = sample_uniform(backend, (10, ))
    assert get_array_module(samples) == backend


@pytest.mark.parametrize("backend", pytest.backends)
def test_sample_gaussian(backend):
    """
    Ensures that array of random samples has array type
    corresponding to the right backend module.
    """
    samples = sample_gaussian(backend, (10, ))
    assert get_array_module(samples) == backend

@pytest.mark.parametrize("backend", pytest.backends)
def test_numel(backend):
    """
    Ensures that the numel function returns the right number of elements.
    """
    array = backend.ones(10)
    assert numel(array) == 10

@pytest.mark.parametrize("backend", pytest.backends)
def test_concatenate(backend):
    """
    Ensures that concatenation of array yields tensor with the expected size.
    """
    array_1 = backend.ones((10, 1))
    array_2 = backend.ones((10, 2))
    result = concatenate(backend, [array_1, array_2], 1)
    assert numel(result) == 30

@pytest.mark.parametrize("backend", pytest.backends)
def test_expand_dims(backend):
    """
    Ensures that expansion of dims yields expected shape.
    """
    array = backend.ones((10,))
    result = expand_dims(backend, array, 1)
    assert len(result.shape) == 2
    assert result.shape[1] == 1

@pytest.mark.parametrize("backend", pytest.backends)
def test_pad_zeros(backend):
    """
    Ensures that zero padding pads zeros.
    """
    array = backend.ones((10, 10))
    result = pad_zeros(backend, array, 2, 1)
    result = pad_zeros(backend, result, 1, 0)
    assert result.shape[0] == 12
    assert result.shape[1] == 14
    assert result[0, 1] == 0.0
    assert result[-1, -2] == 0.0

@pytest.mark.parametrize("backend", pytest.backends)
def test_pad_zeros_left(backend):
    """
    Ensures that zero padding pads zeros only on left side.
    """
    array = backend.ones((10, 10))
    result = pad_zeros_left(backend, array, 2, 1)
    result = pad_zeros_left(backend, result, 1, 0)
    assert result.shape[0] == 11
    assert result.shape[1] == 12
    assert result[0, 1] == 0.0
    assert result[-1, -2] != 0.0

@pytest.mark.parametrize("backend", pytest.backends)
def test_as_type(backend):
    """
    Ensures that conversion of types works.
    """
    array = backend.ones((10, 10))
    mask = array > 0.0
    result = as_type(backend, mask, array)
    assert array.dtype == result.dtype

@pytest.mark.parametrize("backend", pytest.backends)
def test_arange(backend):
    """
    Ensures that generation of ranges works as expected.
    """
    array = arange(backend, 0, 10.1, 1)
    assert array[0] == 0.0
    assert array[-1] == 10.0

@pytest.mark.parametrize("backend", pytest.backends)
def test_reshape(backend):
    array = arange(backend, 0, 10.1, 1)
    result = reshape(backend, array, (1, 11, 1))
    assert result.shape[0] == 1
    assert result.shape[1] == 11
    assert result.shape[2] == 1

@pytest.mark.parametrize("backend", pytest.backends)
def test_trapz(backend):
    array = arange(backend, 0, 10.1, 1)
    result = trapz(backend, array, array, 0)
    assert result == 50

@pytest.mark.parametrize("backend", pytest.backends)
def test_cumsum(backend):
    array = reshape(backend, arange(backend, 0, 10.1, 1), (11, 1))
    result = cumsum(backend, array, 0)
    assert result[-1, 0] == 55
    result = cumsum(backend, array, 1)
    assert result[-1, 0] == 10

@pytest.mark.parametrize("backend", pytest.backends)
def test_cumtrapz(backend):
    y = reshape(backend, arange(backend, 0, 10.1, 1), (11, 1))
    x = arange(backend, 0, 10.1, 1)

    result = cumtrapz(backend, y, x, 0)
    assert result[0, 0] == 0.0
    assert result[-1, 0] == 50.0

    result = cumtrapz(backend, y, 2.0 * x, 0)
    assert result[0, 0] == 0.0
    assert result[-1, 0] == 100.0
