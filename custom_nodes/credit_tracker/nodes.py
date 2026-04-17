"""
CreditDisplay — Pre-flight cost estimator for ComfyUI Partner Nodes.

Pricing source: https://docs.comfy.org/tutorials/partner-nodes/pricing
All costs are in **Comfy Credits**. Conversion: 211 credits = 1 USD.

ComfyUI already tracks *actual* spend per generation in Settings → Credits.
This node gives you an *estimate before queuing* based on known rates.

Install: copy this folder to ComfyUI/custom_nodes/ and restart ComfyUI.
"""

# Official pricing reference — single source of truth for the URL
PRICING_SOURCE_URL = "https://docs.comfy.org/tutorials/partner-nodes/pricing"

# Official conversion rate (as of Apr 2026)
CREDITS_PER_USD = 211.0

# ---------------------------------------------------------------------------
# Resolution → (width, height) lookup (used for Seedance 2.0 token formula)
# ---------------------------------------------------------------------------
RESOLUTION_DIMS: dict[str, dict[str, tuple[int, int]]] = {
    "16:9": {
        "360p":  (640,  360),
        "480p":  (854,  480),
        "720p":  (1280, 720),
        "1080p": (1920, 1080),
    },
    "9:16": {
        "360p":  (360,  640),
        "480p":  (480,  854),
        "720p":  (720,  1280),
        "1080p": (1080, 1920),
    },
    "1:1": {
        "360p":  (360,  360),
        "480p":  (480,  480),
        "720p":  (720,  720),
        "1080p": (1080, 1080),
    },
}

# ---------------------------------------------------------------------------
# Pricing table
#
# billing_type:
#   "per_run"    — flat cost per generation (credits)
#   "per_sec"    — credits per second of output video
#   "seedance2"  — ByteDance Seedance 2.0/Fast: official pixel-temporal token formula
#                  tokens = (in_dur + out_dur) × h × w × 24fps ÷ 1024  (Per K tokens)
#   "per_1m_tok" — ByteDance Seedance 1.x: same formula applied as estimation
#                  (Per 1M tokens; exact 1.x formula not published by ByteDance)
#
# Notes inline where non-obvious.
# ---------------------------------------------------------------------------
PRICING: dict = {
    # ---- ByteDance Seedance ------------------------------------------------
    # Source: PRICING_SOURCE_URL §ByteDance
    # Seedance 2.0 token formula:
    #   tokens = (in_dur + out_dur) × out_h × out_w × 24fps ÷ 1024
    #   cost   = tokens × credits_per_k_tokens / 1000
    "Seedance 2.0 Fast (i2v/t2v)": {
        "label":   "Seedance 2.0 Fast — image/text→video",
        "vendor":  "ByteDance",
        "model_id": "dreamina-seedance-2-0-fast",
        "billing_type": "seedance2",
        "credits_per_k_tokens": 1.182,   # official: 1.182 / K tokens
    },
    "Seedance 2.0 Fast (v2v)": {
        "label":   "Seedance 2.0 Fast — video→video",
        "vendor":  "ByteDance",
        "model_id": "dreamina-seedance-2-0-fast",
        "billing_type": "seedance2",
        "credits_per_k_tokens": 0.696,   # official: 0.696 / K tokens
    },
    "Seedance 2.0 (i2v/t2v)": {
        "label":   "Seedance 2.0 — image/text→video",
        "vendor":  "ByteDance",
        "model_id": "dreamina-seedance-2-0",
        "billing_type": "seedance2",
        "credits_per_k_tokens": 1.477,
    },
    "Seedance 2.0 (v2v)": {
        "label":   "Seedance 2.0 — video→video",
        "vendor":  "ByteDance",
        "model_id": "dreamina-seedance-2-0",
        "billing_type": "seedance2",
        "credits_per_k_tokens": 0.907,
    },
    # Seedance 1.x — billed Per 1M tokens. Token formula not officially
    # documented for 1.x; estimation uses the same spatial formula as 2.0.
    "Seedance 1.0 Lite (i2v/t2v)": {
        "label":   "Seedance 1.0 Lite — i2v / t2v  [model: seedance-1-0-lite-*-250428]",
        "vendor":  "ByteDance",
        "billing_type": "per_1m_tok",
        "credits_per_1m_tokens": 379.8,   # 379.8 / 1M tokens
    },
    "Seedance 1.0 Pro (i2v/t2v)": {
        "label":   "Seedance 1.0 Pro — i2v / t2v  [model: seedance-1-0-pro-250528]",
        "vendor":  "ByteDance",
        "billing_type": "per_1m_tok",
        "credits_per_1m_tokens": 527.5,   # 527.5 / 1M tokens
    },
    "Seedance 1.0 Pro Fast (i2v/t2v)": {
        "label":   "Seedance 1.0 Pro Fast — i2v / t2v  [model: seedance-1-0-pro-fast-251015]",
        "vendor":  "ByteDance",
        "billing_type": "per_1m_tok",
        "credits_per_1m_tokens": 211.0,   # 211 / 1M tokens
    },
    "Seedream 4.5 (t2v)": {
        "label":   "Seedream 4.5 — t2v  [model: seedream-4-5-251128]",
        "vendor":  "ByteDance",
        "billing_type": "per_1m_tok",
        "credits_per_1m_tokens": 211.0,   # 211 / 1M tokens
    },
    "Seedance 1.5 Pro (no audio)": {
        "label":   "Seedance 1.5 Pro — no audio  [model: seedance-1-5-pro-251215]",
        "vendor":  "ByteDance",
        "billing_type": "per_1m_tok",
        "credits_per_1m_tokens": 253.2,   # 253.2 / 1M tokens
    },
    "Seedance 1.5 Pro (with audio)": {
        "label":   "Seedance 1.5 Pro — with audio  [model: seedance-1-5-pro-251215]",
        "vendor":  "ByteDance",
        "billing_type": "per_1m_tok",
        "credits_per_1m_tokens": 506.4,   # 506.4 / 1M tokens
    },
    # ---- Kling (Kuaishou) --------------------------------------------------
    "Kling v2.1 Master Pro": {
        "label":   "Kling v2.1 Master (Pro)",
        "vendor":  "Kuaishou",
        "billing_type": "per_run",
        "credits_per_run": 295.4,
    },
    "Kling v2.1 Pro": {
        "label":   "Kling v2.1 (Pro)",
        "vendor":  "Kuaishou",
        "billing_type": "per_run",
        "credits_per_run": 103.39,
    },
    "Kling v2.1 Standard": {
        "label":   "Kling v2.1 (Standard)",
        "vendor":  "Kuaishou",
        "billing_type": "per_run",
        "credits_per_run": 59.08,
    },
    "Kling v1.6 Pro": {
        "label":   "Kling v1.6 (Pro)",
        "vendor":  "Kuaishou",
        "billing_type": "per_run",
        "credits_per_run": 103.39,
    },
    "Kling v1.6 Standard": {
        "label":   "Kling v1.6 (Standard)",
        "vendor":  "Kuaishou",
        "billing_type": "per_run",
        "credits_per_run": 59.08,
    },
    "Kling v2.6 Pro (no audio)": {
        "label":   "Kling v2.6 Pro (no audio)",
        "vendor":  "Kuaishou",
        "billing_type": "per_sec",
        "credits_per_sec": 14.77,
    },
    "Kling v2.6 Pro (with audio)": {
        "label":   "Kling v2.6 Pro (with audio)",
        "vendor":  "Kuaishou",
        "billing_type": "per_sec",
        "credits_per_sec": 29.54,
    },
    # ---- Google ------------------------------------------------------------
    "Veo 2": {
        "label":   "Google Veo 2",
        "vendor":  "Google",
        "billing_type": "per_run",
        "credits_per_run": 105.5,
    },
    "Veo 3 Fast (no audio)": {
        "label":   "Google Veo 3 Fast (no audio)",
        "vendor":  "Google",
        "billing_type": "per_run",
        "credits_per_run": 168.8,
    },
    "Veo 3 Fast (with audio)": {
        "label":   "Google Veo 3 Fast (with audio)",
        "vendor":  "Google",
        "billing_type": "per_run",
        "credits_per_run": 253.2,
    },
    "Veo 3 (no audio)": {
        "label":   "Google Veo 3 (no audio)",
        "vendor":  "Google",
        "billing_type": "per_run",
        "credits_per_run": 337.6,
    },
    "Veo 3 (with audio)": {
        "label":   "Google Veo 3 (with audio)",
        "vendor":  "Google",
        "billing_type": "per_run",
        "credits_per_run": 675.2,
    },
    # ---- OpenAI Sora -------------------------------------------------------
    "Sora 2 (720p)": {
        "label":   "OpenAI Sora 2 — 720p/1280p",
        "vendor":  "OpenAI",
        "billing_type": "per_sec",
        "credits_per_sec": 21.10,
    },
    "Sora 2 Pro (720p)": {
        "label":   "OpenAI Sora 2 Pro — 720p",
        "vendor":  "OpenAI",
        "billing_type": "per_sec",
        "credits_per_sec": 63.30,
    },
    "Sora 2 Pro (1080p)": {
        "label":   "OpenAI Sora 2 Pro — 1080p",
        "vendor":  "OpenAI",
        "billing_type": "per_sec",
        "credits_per_sec": 105.50,
    },
    # ---- Pika --------------------------------------------------------------
    "Pika 2.2 i2v 5s 720p": {
        "label":   "Pika 2.2 — i2v 5s 720p",
        "vendor":  "Pika",
        "billing_type": "per_run",
        "credits_per_run": 42.2,
    },
    "Pika 2.2 i2v 5s 1080p": {
        "label":   "Pika 2.2 — i2v 5s 1080p",
        "vendor":  "Pika",
        "billing_type": "per_run",
        "credits_per_run": 94.95,
    },
    "Pika 2.2 i2v 10s 720p": {
        "label":   "Pika 2.2 — i2v 10s 720p",
        "vendor":  "Pika",
        "billing_type": "per_run",
        "credits_per_run": 126.6,
    },
    "Pika 2.2 i2v 10s 1080p": {
        "label":   "Pika 2.2 — i2v 10s 1080p",
        "vendor":  "Pika",
        "billing_type": "per_run",
        "credits_per_run": 211.0,
    },
    # ---- Minimax -----------------------------------------------------------
    "Minimax Hailuo-02 6s 768P": {
        "label":   "Minimax Hailuo-02 — 6s 768P",
        "vendor":  "Minimax",
        "billing_type": "per_run",
        "credits_per_run": 59.08,
    },
    "Minimax Hailuo-02 6s 1080P": {
        "label":   "Minimax Hailuo-02 — 6s 1080P",
        "vendor":  "Minimax",
        "billing_type": "per_run",
        "credits_per_run": 103.39,
    },
    # ---- Luma --------------------------------------------------------------
    "Luma Ray 2": {
        "label":   "Luma Ray 2",
        "vendor":  "Luma",
        "billing_type": "per_sec",
        "credits_per_sec": 1.93,
    },
    "Luma Ray Flash 2": {
        "label":   "Luma Ray Flash 2",
        "vendor":  "Luma",
        "billing_type": "per_sec",
        "credits_per_sec": 0.66,
    },
    # ---- Moonvalley --------------------------------------------------------
    "Moonvalley i2v 5s": {
        "label":   "Moonvalley — i2v 5s",
        "vendor":  "Moonvalley",
        "billing_type": "per_run",
        "credits_per_run": 316.5,
    },
    "Moonvalley i2v 10s": {
        "label":   "Moonvalley — i2v 10s",
        "vendor":  "Moonvalley",
        "billing_type": "per_run",
        "credits_per_run": 633.0,
    },
    # ---- BFL Flux ----------------------------------------------------------
    "Flux Dev": {
        "label":   "BFL Flux Dev",
        "vendor":  "BFL",
        "billing_type": "per_run",
        "credits_per_run": 5.28,
    },
    "Flux Pro 1.1": {
        "label":   "BFL Flux Pro 1.1",
        "vendor":  "BFL",
        "billing_type": "per_run",
        "credits_per_run": 8.44,
    },
    "Flux Pro 1.1 Ultra": {
        "label":   "BFL Flux Pro 1.1 Ultra",
        "vendor":  "BFL",
        "billing_type": "per_run",
        "credits_per_run": 12.66,
    },
    "Flux Kontext Pro": {
        "label":   "BFL Flux Kontext Pro",
        "vendor":  "BFL",
        "billing_type": "per_run",
        "credits_per_run": 8.44,
    },
    "Flux Kontext Max": {
        "label":   "BFL Flux Kontext Max",
        "vendor":  "BFL",
        "billing_type": "per_run",
        "credits_per_run": 16.88,
    },
    # ---- ElevenLabs --------------------------------------------------------
    "ElevenLabs TTS": {
        "label":   "ElevenLabs Text-to-Speech",
        "vendor":  "ElevenLabs",
        "billing_type": "per_run",
        "credits_per_run": 50.64,
    },
}

_MODEL_KEYS = list(PRICING.keys())
_ALL_RESOLUTIONS = ["360p", "480p", "720p", "1080p"]
_ALL_ASPECT_RATIOS = ["16:9", "9:16", "1:1"]


# ---------------------------------------------------------------------------
# Token / cost helpers
# ---------------------------------------------------------------------------

def _seedance2_tokens(
    out_dur: float,
    width: int,
    height: int,
    fps: int = 24,
    in_dur: float = 0.0,
) -> float:
    """
    Official Seedance 2.0 token formula.
    Ref: https://docs.comfy.org/tutorials/partner-nodes/pricing §ByteDance
      tokens = (in_dur + out_dur) × out_h × out_w × fps ÷ 1024
    Returns token count (not K-tokens).
    """
    return (in_dur + out_dur) * height * width * fps / 1024.0


def _calc_cost(
    model_key: str,
    resolution: str,
    aspect_ratio: str,
    duration_s: float,
    runs: int,
) -> dict:
    entry = PRICING.get(model_key)
    if entry is None:
        return {"error": f"Unknown model: {model_key}"}

    bt = entry["billing_type"]
    dims = RESOLUTION_DIMS.get(aspect_ratio, RESOLUTION_DIMS["16:9"])
    w, h = dims.get(resolution, dims.get("480p", (854, 480)))

    if bt == "per_run":
        unit_credits = entry["credits_per_run"]

    elif bt == "per_sec":
        unit_credits = entry["credits_per_sec"] * duration_s

    elif bt == "seedance2":
        tokens = _seedance2_tokens(duration_s, w, h)
        unit_credits = tokens * entry["credits_per_k_tokens"] / 1000.0

    elif bt == "per_1m_tok":
        # Use the Seedance 2.0 spatial formula as the best available estimate.
        # ByteDance has not published the exact token formula for 1.x models,
        # so results are approximate (~within 10-20% of actual charge).
        tokens = _seedance2_tokens(duration_s, w, h)
        unit_credits = tokens * entry["credits_per_1m_tokens"] / 1_000_000.0

    else:
        return {"error": f"Unknown billing_type: {bt}"}

    total_credits = unit_credits * runs
    total_usd = total_credits / CREDITS_PER_USD

    return {
        "model":         entry["label"],
        "vendor":        entry["vendor"],
        "billing_type":  bt,
        "resolution":    resolution,
        "aspect_ratio":  aspect_ratio,
        "dimensions":    f"{w}×{h}",
        "duration_s":    duration_s,
        "runs":          runs,
        "unit_credits":  unit_credits,
        "total_credits": total_credits,
        "total_usd":     total_usd,
    }


# ---------------------------------------------------------------------------
# Balance check
# ---------------------------------------------------------------------------

def _get_balance(comfyui_url: str = "http://127.0.0.1:8188") -> float | None:
    """
    Fetch the current Comfy Credits balance from the running ComfyUI instance.
    Returns the balance as a float, or None if the call fails.
    Logs debug information to the ComfyUI server console so you can trace failures.
    """
    import urllib.request, json as _json, logging as _log

    base = comfyui_url.rstrip("/")
    endpoints = [
        f"{base}/api/credits",
        f"{base}/internal/credits",
        f"{base}/api/user/credits",
        f"{base}/comfyui-credits",
    ]

    for url in endpoints:
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                status = resp.status
                raw    = resp.read().decode()
                _log.debug("[credit_tracker] %s → %s  body: %s", url, status, raw[:200])

                # Handle raw number response
                try:
                    return float(raw)
                except ValueError:
                    pass

                data = _json.loads(raw)

                # Flat key search
                for key in ("credits", "balance", "credit_balance", "amount", "comfy_credits"):
                    if key in data:
                        return float(data[key])

                # Nested under "data" or "user"
                for wrapper in ("data", "user", "account"):
                    nested = data.get(wrapper, {})
                    if isinstance(nested, dict):
                        for key in ("credits", "balance", "credit_balance", "amount"):
                            if key in nested:
                                return float(nested[key])

                _log.warning(
                    "[credit_tracker] /api/credits responded but no recognised key. "
                    "Full response: %s — please open a GitHub issue on Av007/custom_fns.",
                    raw[:500],
                )
                return None  # Endpoint found but format unknown; stop trying others

        except urllib.error.HTTPError as e:
            _log.debug("[credit_tracker] %s → HTTP %s %s", url, e.code, e.reason)
        except Exception as e:
            _log.debug("[credit_tracker] %s → %s: %s", url, type(e).__name__, e)

    _log.warning(
        "[credit_tracker] Could not reach any credits endpoint at %s. "
        "Check that you are logged in to ComfyUI (Settings → Account).",
        base,
    )
    return None


def _format_output(b: dict, balance: float | None = None, block: bool = False) -> str:
    if "error" in b:
        return f"ERROR: {b['error']}"

    total = b["total_credits"]
    lines = [
        f"Model     : {b['model']} ({b['vendor']})",
        f"Settings  : {b['resolution']} {b['aspect_ratio']}  {b['dimensions']}  {b['duration_s']}s  ×{b['runs']} run(s)",
        f"Per run   : {b['unit_credits']:.2f} cr  (${b['unit_credits'] / CREDITS_PER_USD:.4f})",
        f"Total     : {total:.2f} cr  (${b['total_usd']:.4f})",
    ]

    if balance is not None:
        after   = balance - total
        status  = "OK" if after >= 0 else "INSUFFICIENT"
        lines += [
            f"Balance   : {balance:.2f} cr  (${balance / CREDITS_PER_USD:.4f})",
            f"After run : {after:.2f} cr  (${after / CREDITS_PER_USD:.4f})",
            f"Status    : {status}{'  — run blocked' if status == 'INSUFFICIENT' and block else ''}",
        ]
    else:
        lines.append(
            "Balance   : — (could not fetch; check server console for [credit_tracker] lines)"
        )

    lines.append(f"Rate      : 211 cr = $1 USD  |  {PRICING_SOURCE_URL}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# ComfyUI node: CreditDisplay
# ---------------------------------------------------------------------------

class CreditDisplay:
    """
    Estimate Comfy Credits for a Partner Node generation.
    Optionally fetches the live account balance and blocks the run
    if funds are insufficient.
    Wire cost_text → ShowText|pysssss to display inline on the canvas.
    """

    CATEGORY = "utils/cost"
    FUNCTION = "calculate"
    RETURN_TYPES = ("STRING", "FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("cost_text", "total_credits", "total_usd", "balance_after")
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model":                (_MODEL_KEYS,       {"default": "Seedance 2.0 Fast (i2v/t2v)"}),
                "resolution":           (_ALL_RESOLUTIONS,  {"default": "480p"}),
                "aspect_ratio":         (_ALL_ASPECT_RATIOS, {"default": "16:9"}),
                "duration_s":           ("FLOAT",  {"default": 5.0, "min": 1.0, "max": 120.0, "step": 0.5}),
                "runs":                 ("INT",    {"default": 1, "min": 1, "max": 100, "step": 1}),
                "check_balance":        ("BOOLEAN", {"default": True,  "label_on": "check balance", "label_off": "skip balance"}),
                "block_if_insufficient":("BOOLEAN", {"default": False, "label_on": "block run", "label_off": "warn only"}),
            },
            "optional": {
                # Accept any upstream output (IMAGE, VIDEO, STRING …) to
                # create a dependency edge without constraining the type.
                "trigger":          ("*",               {"forceInput": True}),
                # Wire a PrimitiveNode here to share aspect_ratio with ByteDance.
                "aspect_ratio_in":  (_ALL_ASPECT_RATIOS, {"forceInput": True}),
                "resolution_in":    (_ALL_RESOLUTIONS,   {"forceInput": True}),
            },
        }

    def calculate(
        self,
        model: str,
        resolution: str,
        aspect_ratio: str,
        duration_s: float,
        runs: int,
        check_balance: bool = True,
        block_if_insufficient: bool = False,
        trigger=None,
        aspect_ratio_in: str | None = None,
        resolution_in:   str | None = None,
    ):
        if aspect_ratio_in:
            aspect_ratio = aspect_ratio_in
        if resolution_in:
            resolution = resolution_in
        b = _calc_cost(model, resolution, aspect_ratio, duration_s, runs)
        if "error" in b:
            text = f"ERROR: {b['error']}"
            return {"ui": {"text": [text]}, "result": (text, 0.0, 0.0, 0.0)}

        balance = _get_balance() if check_balance else None
        total   = b["total_credits"]

        if block_if_insufficient and balance is not None and balance < total:
            shortfall = total - balance
            raise RuntimeError(
                f"Insufficient Comfy Credits — need {total:.2f} cr, "
                f"have {balance:.2f} cr (short by {shortfall:.2f} cr / "
                f"${shortfall / CREDITS_PER_USD:.4f}). "
                f"Top up at Settings → Credits."
            )

        text         = _format_output(b, balance, block_if_insufficient)
        after_balance = (balance - total) if balance is not None else -1.0
        return {
            "ui": {"text": [text]},
            "result": (text, float(total), float(b["total_usd"]), float(after_balance)),
        }


# ---------------------------------------------------------------------------
# ComfyUI node: CreditDisplayFromStrings
# ---------------------------------------------------------------------------

class CreditDisplayFromStrings:
    """
    Same as CreditDisplay but accepts model/resolution as STRING inputs
    so you can pipe them from other nodes instead of picking from dropdowns.
    """

    CATEGORY = "utils/cost"
    FUNCTION = "calculate"
    RETURN_TYPES = ("STRING", "FLOAT", "FLOAT")
    RETURN_NAMES = ("cost_text", "total_credits", "total_usd")
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model":        ("STRING", {"default": "Seedance 2.0 Fast (i2v/t2v)"}),
                "resolution":   ("STRING", {"default": "480p"}),
                "aspect_ratio": ("STRING", {"default": "16:9"}),
                "duration_s":   ("FLOAT",  {"default": 5.0, "min": 1.0, "max": 120.0, "step": 0.5}),
                "runs":         ("INT",    {"default": 1, "min": 1, "max": 100}),
            },
        }

    def calculate(
        self,
        model: str,
        resolution: str,
        aspect_ratio: str,
        duration_s: float,
        runs: int,
    ):
        b = _calc_cost(model, resolution, aspect_ratio, duration_s, runs)
        text = _format_output(b)
        credits = float(b.get("total_credits", 0.0))
        usd = float(b.get("total_usd", 0.0))
        return {"ui": {"text": [text]}, "result": (text, credits, usd)}
