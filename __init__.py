"""
ComfyUI custom node entry point.
Loaded by ComfyUI when this repo is cloned into custom_nodes/ (as custom_fns/).
Adds the repo's own custom_nodes/ subfolder to sys.path so credit_tracker
is importable as a proper package with relative imports intact.
"""

import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_pkg_parent = os.path.join(_here, "custom_nodes")
if _pkg_parent not in sys.path:
    sys.path.insert(0, _pkg_parent)

from credit_tracker import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS  # noqa: E402

# Path is relative to THIS file so ComfyUI serves the JS extension correctly
# whether the repo is installed as custom_fns/ or credit_tracker/ directly.
WEB_DIRECTORY = "./custom_nodes/credit_tracker/js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
