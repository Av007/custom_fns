# custom — ComfyUI Custom Nodes

This repository contains custom nodes for [ComfyUI](https://github.com/comfyanonymous/ComfyUI).

## Installation

Copy the desired folder(s) from `custom_nodes/` into your ComfyUI installation's `custom_nodes/` directory, then restart ComfyUI:

```bash
cp -r custom_nodes/credit_tracker /path/to/ComfyUI/custom_nodes/
```

Or clone this repo directly inside `ComfyUI/custom_nodes/` and restart:

```bash
cd /path/to/ComfyUI/custom_nodes
git clone <this-repo-url> comfyui-credit-tracker
```

No `pip install` is required — the package uses Python stdlib only.

---

## Nodes

### `credit_tracker` — Pre-flight cost estimator

Shows the estimated **Comfy Credits** (and USD equivalent) for a Partner Node generation *before* you queue it. Wire the output into a `ShowText|pysssss` node to display the cost inline on the canvas.

> ComfyUI already tracks *actual* spend per generation in **Settings → Credits**. This node gives you an estimate *before* queuing so you can catch expensive configurations early.

#### ComfyUI nodes registered

| Node | Category | Use |
|---|---|---|
| `Credit Display` | `utils/cost` | Dropdown pickers for model, resolution, aspect ratio, duration, runs |
| `Credit Display (from strings)` | `utils/cost` | Same calculation but accepts raw STRING inputs — pipe values from other nodes |

Both nodes output:

| Output | Type | Description |
|---|---|---|
| `cost_text` | STRING | Formatted multi-line summary → wire to `ShowText\|pysssss` |
| `total_credits` | FLOAT | Total Comfy Credits |
| `total_usd` | FLOAT | USD equivalent (`total_credits ÷ 211`) |

#### Connecting to ShowText

```
[CreditDisplay] ──cost_text──► [ShowText|pysssss]
```

Requires [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts) for `ShowText|pysssss`.

#### Example output (Seedance 2.0 Fast, 480p 16:9, 5 s)

```
Model     : Seedance 2.0 Fast — image/text→video (ByteDance)
Settings  : 480p 16:9  854×480  5.0s  ×1 run(s)
Per run   : 56.78 cr  ($0.2691)
Total     : 56.78 cr  ($0.2691)
Rate      : 211 cr = $1 USD  |  https://docs.comfy.org/tutorials/partner-nodes/pricing
```

#### Supported models (41 total)

Pricing source: <https://docs.comfy.org/tutorials/partner-nodes/pricing>  
Conversion: **211 Comfy Credits = 1 USD**

##### ByteDance

| Model key | Rate | Billing |
|---|---|---|
| Seedance 2.0 Fast (i2v/t2v) | 1.182 cr / K tokens | pixel-temporal formula |
| Seedance 2.0 Fast (v2v) | 0.696 cr / K tokens | pixel-temporal formula |
| Seedance 2.0 (i2v/t2v) | 1.477 cr / K tokens | pixel-temporal formula |
| Seedance 2.0 (v2v) | 0.907 cr / K tokens | pixel-temporal formula |
| Seedance 1.5 Pro (no audio) | 253.2 cr / 1M tokens | estimated |
| Seedance 1.5 Pro (with audio) | 506.4 cr / 1M tokens | estimated |
| Seedance 1.0 Pro (i2v/t2v) | 527.5 cr / 1M tokens | estimated |
| Seedance 1.0 Pro Fast (i2v/t2v) | 211.0 cr / 1M tokens | estimated |
| Seedance 1.0 Lite (i2v/t2v) | 379.8 cr / 1M tokens | estimated |
| Seedream 4.5 (t2v) | 211.0 cr / 1M tokens | estimated |

> **Seedance 2.0 token formula** (official):  
> `tokens = (in_dur + out_dur) × height × width × 24fps ÷ 1024`  
> When input is text, image, or audio, `in_dur = 0`.  
> **Seedance 1.x** token formula is not published by ByteDance; the same formula is used as a best estimate (within ~10–20%).

##### Kuaishou (Kling)

| Model key | Rate | Billing |
|---|---|---|
| Kling v2.1 Master Pro | 295.4 cr / run | flat |
| Kling v2.1 Pro | 103.39 cr / run | flat |
| Kling v2.1 Standard | 59.08 cr / run | flat |
| Kling v1.6 Pro | 103.39 cr / run | flat |
| Kling v1.6 Standard | 59.08 cr / run | flat |
| Kling v2.6 Pro (no audio) | 14.77 cr / sec | per second |
| Kling v2.6 Pro (with audio) | 29.54 cr / sec | per second |

##### Google

| Model key | Rate | Billing |
|---|---|---|
| Veo 2 | 105.5 cr / run | flat |
| Veo 3 Fast (no audio) | 168.8 cr / run | flat |
| Veo 3 Fast (with audio) | 253.2 cr / run | flat |
| Veo 3 (no audio) | 337.6 cr / run | flat |
| Veo 3 (with audio) | 675.2 cr / run | flat |

##### OpenAI

| Model key | Rate | Billing |
|---|---|---|
| Sora 2 (720p) | 21.10 cr / sec | per second |
| Sora 2 Pro (720p) | 63.30 cr / sec | per second |
| Sora 2 Pro (1080p) | 105.50 cr / sec | per second |

##### Pika

| Model key | Rate | Billing |
|---|---|---|
| Pika 2.2 i2v 5s 720p | 42.2 cr / run | flat |
| Pika 2.2 i2v 5s 1080p | 94.95 cr / run | flat |
| Pika 2.2 i2v 10s 720p | 126.6 cr / run | flat |
| Pika 2.2 i2v 10s 1080p | 211.0 cr / run | flat |

##### Minimax

| Model key | Rate | Billing |
|---|---|---|
| Minimax Hailuo-02 6s 768P | 59.08 cr / run | flat |
| Minimax Hailuo-02 6s 1080P | 103.39 cr / run | flat |

##### Luma

| Model key | Rate | Billing |
|---|---|---|
| Luma Ray 2 | 1.93 cr / sec | per second |
| Luma Ray Flash 2 | 0.66 cr / sec | per second |

##### Moonvalley

| Model key | Rate | Billing |
|---|---|---|
| Moonvalley i2v 5s | 316.5 cr / run | flat |
| Moonvalley i2v 10s | 633.0 cr / run | flat |

##### BFL (Flux)

| Model key | Rate | Billing |
|---|---|---|
| Flux Dev | 5.28 cr / run | flat |
| Flux Pro 1.1 | 8.44 cr / run | flat |
| Flux Pro 1.1 Ultra | 12.66 cr / run | flat |
| Flux Kontext Pro | 8.44 cr / run | flat |
| Flux Kontext Max | 16.88 cr / run | flat |

##### ElevenLabs

| Model key | Rate | Billing |
|---|---|---|
| ElevenLabs TTS | 50.64 cr / run | flat |

---

## Updating prices

All rates live in the `PRICING` dict at the top of `custom_nodes/credit_tracker/nodes.py`. When ComfyUI updates its official pricing page, edit the relevant `credits_per_*` value and restart ComfyUI — no other changes needed.

Official source: <https://docs.comfy.org/tutorials/partner-nodes/pricing>

---

## File structure

```
custom/
└── custom_nodes/
    └── credit_tracker/
        ├── __init__.py   # registers nodes with ComfyUI
        └── nodes.py      # all logic, pricing table, node classes
```

## Portability

The package has **no external dependencies** (pure Python stdlib). To deploy to another ComfyUI instance:

```bash
# Option A — rsync
rsync -avz custom_nodes/credit_tracker/ user@remote:/path/to/ComfyUI/custom_nodes/credit_tracker/

# Option B — git clone on the target machine
cd /path/to/ComfyUI/custom_nodes
git clone <this-repo-url> credit_tracker

# Option C — ComfyUI Manager → Install via Git URL
```

The workflow JSON (`projects/seedance.json`) references the node by `type: "CreditDisplay"` which matches the key in `NODE_CLASS_MAPPINGS`. As long as the package is installed, the workflow loads cleanly on any ComfyUI instance.
