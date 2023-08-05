# -*- coding: utf-8 -*-

import warnings


__version__ = "0.0.0.git"
try:
    from pkg_resources import get_distribution, DistributionNotFound

    __version__ = get_distribution("tuxsuite").version
except ImportError:
    warnings.warn(
        UserWarning(
            "tuxsuite needs pkg_resources to determine it's own version number, but that is not available"
        )
    )
except DistributionNotFound:
    warnings.warn(UserWarning("tuxsuite not installed, can't determine version number"))
    pass
