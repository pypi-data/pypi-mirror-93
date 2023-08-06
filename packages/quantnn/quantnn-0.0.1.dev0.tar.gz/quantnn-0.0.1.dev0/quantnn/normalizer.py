"""
==================
quantnn.normalizer
==================

This module provides a simple normalizer class, which can be used
to normalize input data and store the normalization data.
"""
import pickle

import numpy as np
from quantnn.files import read_file


class Normalizer:
    """
    The Normalizer class can be used to normalize input data to a neural
    network. On creation, it computes mean and standard deviation of the
    provided input data and stores it so that it can be applied to other
    datasets.
    """
    def __init__(self,
                 x,
                 exclude_indices=None,
                 feature_axis=1):
        """
        Create Normalizer object for given input data.

        Arguments:
            x: Tensor containing the input data.
            exclude_indices: List of integer containing feature indices
                that should not be normalized.
            feature_axis: The axis along which the input features are located.
        """
        x = x.astype(np.float64)

        n = x.shape[feature_axis]
        self.means = {}
        self.std_devs = {}

        if exclude_indices is None:
            self.exclude_indices = []
        else:
            self.exclude_indices = exclude_indices
        self.feature_axis = feature_axis
        selection = [slice(0, None)] * len(x.shape)

        indices = [i for i in range(n) if i not in self.exclude_indices]
        for i in indices:
            selection[feature_axis] = i
            self.means[i] = x[tuple(selection)].mean()
            self.std_devs[i] = x[tuple(selection)].std()

    def __call__(self, x):
        """
        Applies normalizer to input data.

        Args:
            x: The input tensor to normalize.

        Returns:
            The input tensor x normalized using the normalization data
            of this normalizer object.
        """
        normalized = []
        n = x.shape[self.feature_axis]
        selection = [slice(0, None)] * len(x.shape)

        for i in range(n):
            selection[self.feature_axis] = i
            if i in self.means:
                x_slice = x[tuple(selection)].astype(np.float64)
                if np.isclose(self.std_devs[i], 0.0):
                    x_normed = -1.0 * np.ones_like(x_slice)
                else:
                    x_normed = ((x_slice - self.means[i]) / self.std_devs[i])
            else:
                x_normed = x[tuple(selection)]
            x_normed = np.expand_dims(x_normed, self.feature_axis)
            normalized.append(x_normed.astype(np.float32))

        return np.concatenate(normalized, self.feature_axis)

    @staticmethod
    def load(filename):
        """
        Load normalizer from file.

        Args:
            filename: The path to the file containing the normalizer.

        Returns:
            The loaded Normalizer object
        """
        with read_file(filename, "rb") as file:
            return pickle.load(file)

    def save(self, filename):
        """
        Store normalizer to file.

        Saves normalizer to a file using pickle.

        Args:
            filename: The file to which to store the normalizer.
        """
        with open(filename, "wb") as file:
            pickle.dump(self, file)
