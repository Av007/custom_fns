# Credit Display — ComfyUI Plugin

**What it does:** Shows how much a video generation will cost *before* you click Run.

---

## Why use it?

When you run AI video generation through ComfyUI (Seedance, Kling, Veo, Sora, etc.), each generation spends **Comfy Credits** from your account. The cost changes depending on the model, resolution, and duration you pick — and it's easy to accidentally run something expensive.

**Credit Display** shows the estimated cost as soon as you change any setting, so there are no surprises on your bill.

---

## What it looks like on the canvas

```
┌─────────────────────────────────────────────┐
│  Credit Display                             │
│                                             │
│  Model      Seedance 2.0 Fast (i2v/t2v) ▾  │
│  Resolution 480p ▾    Aspect 16:9 ▾         │
│  Duration   5.0 s     Runs  1               │
└─────────────────────────────────────────────┘
           │ cost_text
           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Show Text                                                      │
│                                                                 │
│  Model     : Seedance 2.0 Fast — image/text→video (ByteDance)  │
│  Settings  : 480p 16:9  854×480  5.0s  ×1 run(s)              │
│  Per run   : 56.78 cr  ($0.27)                                  │
│  Total     : 56.78 cr  ($0.27)                                  │
│  Balance   : 1024.00 cr  ($4.85)                                │
│  After run : 967.22 cr  ($4.58)                                 │
│  Status    : OK                                                 │
│  Rate      : 211 cr = $1 USD                                    │
└─────────────────────────────────────────────────────────────────┘
```

The text updates **instantly** when you change any dropdown — no need to run the workflow first.

---

## How to read the output

| Line | Meaning |
|---|---|
| **Model** | Which AI model and vendor will be charged |
| **Settings** | Resolution, aspect ratio, pixel size, duration, number of runs |
| **Per run** | Cost of a single generation in credits and USD |
| **Total** | Per run × number of runs |
| **Balance** | Your current Comfy Credits (fetched from ComfyUI) |
| **After run** | Credits remaining once this generation is billed |
| **Status** | `OK` when affordable; `INSUFFICIENT` otherwise |
| **Rate** | The official conversion rate (211 Comfy Credits = $1 USD) |

> **Comfy Credits** are the in-app currency. You buy them in **Settings → Credits** inside ComfyUI. They never expire if you top up (top-up credits last 1 year).

---

## Supported models

| Vendor | Models |
|---|---|
| **ByteDance** | Seedance 2.0, Seedance 2.0 Fast, Seedance 1.5 Pro, Seedance 1.0 Pro/Lite, Seedream 4.5 |
| **Kuaishou** | Kling v1.6, v2.1, v2.6 (Pro / Standard / Master) |
| **Google** | Veo 2, Veo 3, Veo 3 Fast (with and without audio) |
| **OpenAI** | Sora 2, Sora 2 Pro |
| **Pika** | Pika 2.2 (5s and 10s, 720p and 1080p) |
| **Minimax** | Hailuo-02 |
| **Luma** | Ray 2, Ray Flash 2 |
| **Moonvalley** | i2v 5s and 10s |
| **BFL** | Flux Dev, Pro 1.1, Pro 1.1 Ultra, Kontext Pro/Max |
| **ElevenLabs** | Text-to-Speech |

Prices are sourced from the official ComfyUI pricing page:
https://docs.comfy.org/tutorials/partner-nodes/pricing

---

## How to install

> Ask your server admin to run this once on the ComfyUI server, then restart ComfyUI.

```
cd ComfyUI/custom_nodes
git clone https://github.com/Av007/custom_fns.git custom_fns
```

To update to the latest prices later:

```
cd ComfyUI/custom_nodes/custom_fns
git pull
```

Then restart ComfyUI.

---

## How to add it to a workflow

1. Right-click on the canvas → **Add Node → utils/cost → Credit Display**
2. Set **Model**, **Resolution**, **Aspect Ratio**, **Duration**, and **Runs** to match your generation node
3. Right-click on the canvas → **Add Node → utils → Show Text** (requires ComfyUI Custom Scripts)
4. Connect **cost\_text** output of Credit Display → **text** input of Show Text
5. The cost appears immediately and updates as you change settings

---

## Important notes

- **This is an estimate.** Actual charges may vary slightly, especially for Seedance 1.x models (their exact token formula is not publicly documented).
- **Actual spend** is always visible after generation in **Settings → Credits → Credit History** inside ComfyUI.
- **Balance check** calls the local ComfyUI API (`/api/credits` etc.) on your own machine — it never talks to any third-party server.
- **Block-on-insufficient** is opt-in. When enabled, the workflow stops before the paid node runs, so no credits are spent on a failed queue.
- The plugin has **no external dependencies** — pure Python standard library, works on any OS.

---

## Prices changed — what to do?

If ComfyUI updates its pricing, the numbers can be corrected without a developer:

1. Open the file `ComfyUI/custom_nodes/custom_fns/custom_nodes/credit_tracker/nodes.py`
2. Find the model name in the `PRICING` section near the top
3. Update the number next to `credits_per_run`, `credits_per_sec`, or `credits_per_k_tokens`
4. Restart ComfyUI

The same change also needs to be made in `custom_nodes/credit_tracker/js/credit_display.js` for the live display to match.

---

*Plugin source: https://github.com/Av007/custom_fns*
*Pricing reference: https://docs.comfy.org/tutorials/partner-nodes/pricing*
