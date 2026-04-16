"""
credit_tracker — ComfyUI custom node package
Install: copy this folder to ComfyUI/custom_nodes/ and restart ComfyUI.
"""

from .nodes import CreditDisplay, CreditDisplayFromStrings

NODE_CLASS_MAPPINGS = {
    "CreditDisplay":            CreditDisplay,
    "CreditDisplayFromStrings": CreditDisplayFromStrings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreditDisplay":            "Credit Display",
    "CreditDisplayFromStrings": "Credit Display (from strings)",
}

# Tells ComfyUI to serve js/ as static assets so the live-update
# extension (credit_display.js) loads automatically in the browser.
WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
