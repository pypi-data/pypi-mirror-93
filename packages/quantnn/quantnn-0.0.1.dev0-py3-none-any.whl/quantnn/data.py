from collections import OrderedDict
from collections.abc import Iterable, Mapping
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from queue import Queue
import tempfile

import numpy as np
from quantnn.common import DatasetError
from quantnn.files import sftp

_DATASET_LOCK = multiprocessing.Lock()


def iterate_dataset(dataset):
    """
    Turns an iterable or sequence dataset into a generator.

    Returns:

        Generator object providing access to the batches in the dataset.

    Raises:

        quantnn.DatasetError when the dataset is neither iterable nor
        a sequence.

    """
    if isinstance(dataset, Iterable):
        yield from dataset
    elif hasattr(dataset, "__len__") and hasattr(dataset, "__getitem__"):
        for i in range(len(dataset)):
            yield dataset[i]
    else:
        raise DatasetError("The provided dataset is neither iterable nor "
                           "a sequence.")


def open_dataset(host,
                 path,
                 dataset_factory,
                 args=None,
                 kwargs=None):
    """
    Downloads file using SFTP and opens dataset using a temporary directory
    for file transfer.

    Args:
        host: IP address of the host.
        path: The path for which to list the files
        dataset_class: The class used to read in the file.
        args: List of positional arguments passed to the dataset_factory method
              after the downloaded file.
        kwargs: Dictionary of keyword arguments passed to the dataset
            factory call.

    Returns:
        An object created using the provided dataset_factory
        using the downloaded file as first arguments and the provided
        args and kwargs as positional and keyword arguments.
    """
    if args is None:
        args = []
    if not isinstance(args, Iterable):
        raise ValueError("Provided postitional arguments 'args' must be "
                         "iterable.")
    if kwargs is None:
        kwargs = {}
    if not isinstance(kwargs, Mapping):
        raise ValueError("Provided postitional arguments 'kwargs' must be "
                         "a mapping.")

    with sftp.download_file(host, path) as file:
        dataset = dataset_factory(file, *args, **kwargs)
    return dataset


class SFTPStream:
    """
    Datset class to stream data via SFTP.

    This class can be used to iterate over multiple datasets located
    on a remote machine that is accessible via SFTP. It provides an
    iterable over the batches in all of the files in that folder.


    """
    def __init__(self,
                 host,
                 path,
                 dataset_factory,
                 args=None,
                 kwargs=None,
                 n_workers=4,
                 n_files=None):
        """
        Create new SFTPStream dataset.

        Args:
            host: The IP address of the host as string.
            path: The path on the SFTP server where the datasets are located.
            dataset_factory: The function used to construct the dataset
                 instances for each file.
            args: Additional, positional arguments passed to
                 ``dataset_factory`` following the local file path of the
                 local copy of the dataset file.
            kwargs: Dictionary of keyword arguments passed to the dataset
                 factory.
        """
        self.host = host
        self.path = path
        self.dataset_factory = dataset_factory
        self.args = args
        self.kwargs = kwargs
        self.n_workers = n_workers
        self.files = sftp.list_files(self.host, self.path)
        if n_files is not None:
            self.files = self.files[:n_files]

        # Sort datasets into random order.
        self.epoch_queue = Queue()
        self.active_queue = Queue()
        self.cache = OrderedDict()
        self.pool = ProcessPoolExecutor(max_workers=self.n_workers)
        self._prefetch()

    def _prefetch(self):
        if self.epoch_queue.empty():
            for f in np.random.permutation(self.files):
                self.epoch_queue.put(f)

        for i in range(self.n_workers):

            if not self.epoch_queue.empty():

                file = self.epoch_queue.get()
                self.active_queue.put(file)

                if file in self.cache:
                    continue
                else:
                    if len(self.cache) > self.n_workers:
                        self.cache.popitem(last=False)
                    arguments = [self.host, file, self.dataset_factory,
                                 self.args, self.kwargs]
                    self.cache[file] = self.pool.submit(open_dataset, *arguments)

    def get_next_dataset(self):
        """
        Returns the next dataset of the current epoch and issues the prefetch
        of the following data.

        Returns:
            The dataset instance that is the next in the random sequence
            of the current epoch.
        """

        #
        # Prepare download of next file.
        #

        if self.epoch_queue.empty():
            for f in np.random.permutation(self.files):
                self.epoch_queue.put(f)

        file = self.epoch_queue.get()
        self.active_queue.put(file)

        if file in self.cache:
            self.cache.move_to_end(file)
        else:
            if len(self.cache) > self.n_workers:
                self.cache.popitem(last=False)
            arguments = [self.host, file, self.dataset_factory,
                            self.args, self.kwargs]
            self.cache[file] = self.pool.submit(open_dataset, *arguments)

        #
        # Return current file.
        #

        file = self.active_queue.get()
        dataset = self.cache[file].result()

        return dataset


    def __iter__(self):
        """
        Iterate over all batches in all remote files.
        """
        for _ in self.files:
            dataset = self.get_next_dataset()
            yield from iterate_dataset(dataset)
