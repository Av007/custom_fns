"""
credit_tracker — ComfyUI custom node package
Install: copy this folder to ComfyUI/custom_nodes/ and restart ComfyUI.
"""

from .nodes import CreditDisplay, CreditDisplayFromStrings, AspectCrop

NODE_CLASS_MAPPINGS = {
    "CreditDisplay":            CreditDisplay,
    "CreditDisplayFromStrings": CreditDisplayFromStrings,
    "AspectCrop":               AspectCrop,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CreditDisplay":            "Credit Display",
    "CreditDisplayFromStrings": "Credit Display (from strings)",
    "AspectCrop":               "Aspect Crop",
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
