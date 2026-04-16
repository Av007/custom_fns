# ComfyUI custom node entry point.
# Loaded by ComfyUI when this repo is cloned into custom_nodes/ (as custom_fns/).
# Adds the repo's own custom_nodes/ subfolder to sys.path so that
# `credit_tracker` is importable as a proper package (relative imports intact).

import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_pkg_parent = os.path.join(_here, "custom_nodes")

if _pkg_parent not in sys.path:
    sys.path.insert(0, _pkg_parent)

from credit_tracker import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS  # noqa: E402

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
