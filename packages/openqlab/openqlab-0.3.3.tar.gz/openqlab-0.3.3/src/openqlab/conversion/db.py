import warnings

import numpy as np

try:
    from uncertainties import umath, core

    UNCERTAINTIES = True
except ImportError:
    UNCERTAINTIES = False


def to_lin(data):
    return 10 ** (data / 10.0)


def from_lin(data):
    if UNCERTAINTIES and isinstance(data, (core.Variable, core.AffineScalarFunc)):
        log10 = umath.log10  # pylint: disable=no-member
    else:
        log10 = np.log10
    return 10 * log10(data)


def mean(data, axis=None):
    return from_lin(np.mean(to_lin(data), axis=axis))


def subtract(signal, noise):
    return from_lin(to_lin(signal) - to_lin(noise))


def average(datasets):
    warnings.warn(
        "Use `openqlab.conversion.de.mean` with argument 'axis=-1' instead",
        DeprecationWarning,
    )
    lin = to_lin(datasets)
    average = np.sum(lin, 0) / len(lin)
    return from_lin(average)


def dBm2Vrms(dbm, R=50.0):
    return np.sqrt(0.001 * R) * 10 ** (dbm / 20)
