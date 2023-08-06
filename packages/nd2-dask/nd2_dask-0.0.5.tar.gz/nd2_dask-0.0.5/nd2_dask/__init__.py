try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

# replace the asterisk with named imports
from .nd2_reader import napari_get_nd2_reader


__all__ = ["napari_get_reader"]
