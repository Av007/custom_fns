# ComfyUI custom node entry point.
# This file sits at the repo root so ComfyUI finds it when the repo is
# cloned directly into custom_nodes/ (e.g. as custom_nodes/custom_fns/).
# It re-exports the node mappings from the nested package.

from custom_nodes.credit_tracker import (
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS,
)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
