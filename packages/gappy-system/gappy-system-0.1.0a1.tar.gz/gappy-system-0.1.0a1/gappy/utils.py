# ****************************************************************************
#       Copyright (C) 2006 William Stein <wstein@gmail.com>
#       Copyright (C) 2021 E. Madison Bray <embray@lri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

import resource
import sys

import psutil


_SPECIAL_ATTRS = set([
    '_ipython_canary_method_should_not_exist_',
    '_repr_mimebundle_'
])
"""
Special attributes which should not be looked up in GAP.

Mostly intended to prevent IPython's custom display hook from unintentially
initializing the GAP interpreter.
"""
# _repr_mimebundle_ should not be needed here; this seems to be a bug in
# Ipython


def get_gap_memory_pool_size(unit='m'):
    """
    Get the gap memory pool size for new GAP processes.

    Examples
    --------

    >>> from gappy.utils import get_gap_memory_pool_size
    >>> get_gap_memory_pool_size()  # system-specific output
    '...m'
    """
    allowed_units = ('k', 'm', 'g')
    unit = unit.lower()

    if unit not in allowed_units:
        raise ValueError(f'unit must be one of {", ".join(allowed_units)}')

    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    vmax = virtual_memory_limit()

    suggested_size = max(swap.free // 10, mem.available // 50)
    # Don't eat all address space if the user set ulimit -v
    suggested_size = min(suggested_size, vmax // 10)
    # ~220MB is the minimum for long doctests
    suggested_size = max(suggested_size, 400 * 1024**2)
    unit_bytes = 1024**(allowed_units.index(unit) + 1)
    suggested_size //= unit_bytes
    return str(suggested_size) + unit


def virtual_memory_limit():
    """
    Return the upper limit for virtual memory usage.

    This is the value set by ``ulimit -v`` at the command line or a
    practical limit if no limit is set. In any case, the value is
    bounded by ``sys.maxsize``.

    Returns
    -------

    int
        The virtual memory limit in bytes.

    Examples
    --------

    >>> from gappy.utils import virtual_memory_limit
    >>> virtual_memory_limit() > 0
    True
    >>> virtual_memory_limit() <= sys.maxsize
    True
    """
    try:
        vmax = resource.getrlimit(resource.RLIMIT_AS)[0]
    except resource.error:
        vmax = resource.RLIM_INFINITY
    if vmax == resource.RLIM_INFINITY:
        vmax = psutil.virtual_memory().total + psutil.swap_memory().total
    return min(vmax, sys.maxsize)
