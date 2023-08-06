"""Simple squeezing calculations."""

import logging
from typing import Union

import numpy as np

from openqlab.conversion import db

log = logging.getLogger(__name__)


try:
    from uncertainties import ufloat, umath, core

    _DATA_TYPES = Union[float, list, np.array, ufloat]
    UNCERTAINTIES = True
    log.info("uncertainties imported")
except ImportError:
    _DATA_TYPES = Union[float, list, np.array]  # type: ignore
    UNCERTAINTIES = False
    log.info("uncertainties not imported")


def losses(sqz: _DATA_TYPES, anti_sqz: _DATA_TYPES):
    """Calculate losses from known squeezing and anti-squeezing levels.

    Parameters
    ----------
    sqz : float, :obj:`numpy.array`
        The squeezing level (negative value, because it is below vacuum).
    anti_sqz : float, :obj:`numpy.array`
        The anti-squeezing level (positive value, because it is above vacuum).
    """
    sqz = _ensure_np_array(sqz)
    anti_sqz = _ensure_np_array(anti_sqz)

    L = (1 - db.to_lin(sqz) * db.to_lin(anti_sqz)) / (
        2 - db.to_lin(sqz) - db.to_lin(anti_sqz)
    )
    return L


def initial(sqz: _DATA_TYPES, anti_sqz: _DATA_TYPES):
    """Calculate the initial squeezing level from known squeezing and anti-squeezing levels.

    Parameters
    ----------
    sqz : float, :obj:`numpy.array`
        The squeezing level (negative value, because it is below vacuum).
    anti_sqz : float, :obj:`numpy.array`
        The anti-squeezing level (positive value, because it is above vacuum).
    """
    log.debug(f"UNCERTAINTIES: {UNCERTAINTIES}")
    if (
        UNCERTAINTIES
        and isinstance(sqz, (core.Variable, core.AffineScalarFunc))
        and isinstance(anti_sqz, (core.Variable, core.AffineScalarFunc))
    ):
        log10 = umath.log10  # pylint: disable=no-member
        log.debug("umath.log10")
    else:
        log10 = np.log10
        log.debug("np.log10")

    sqz = _ensure_np_array(sqz)
    anti_sqz = _ensure_np_array(anti_sqz)

    L = losses(sqz, anti_sqz)
    initial_sqz = 10 * log10((db.to_lin(anti_sqz) - L) / (1 - L))
    return initial_sqz


def max(loss: _DATA_TYPES):
    """Calculate the maximum possible squeezing level with given loss.

    Parameters
    ----------
    loss : float, :obj:`numpy.array`
        Level of losses (number, relative to 1).
    """
    loss = _ensure_np_array(loss)

    return db.from_lin(db.to_lin(-100) * (1 - loss) + loss)


def _ensure_np_array(value):
    if isinstance(value, list):
        return np.asarray(value)
    return value
